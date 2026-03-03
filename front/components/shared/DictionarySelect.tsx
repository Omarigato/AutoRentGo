"use client";

import { useState, useEffect, useMemo, useRef } from "react";
import { Search, ChevronDown, Check, Loader2, AlertCircle } from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { useInfiniteDictionaries } from "@/hooks/useDictionaries";
import { cn } from "@/lib/utils";
import { useTranslation } from "@/hooks/useTranslation";

interface DictionarySelectProps {
    type: string;
    parentId?: number;
    value: string | null;
    onChange: (value: string | null) => void;
    placeholder?: string;
    label?: string;
    disabled?: boolean;
    required?: boolean;
}

export function DictionarySelect({
    type,
    parentId,
    value,
    onChange,
    placeholder = "Выберите...",
    label,
    disabled = false,
    required = false,
}: DictionarySelectProps) {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState("");
    const [debouncedSearch, setDebouncedSearch] = useState("");
    const scrollEndRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    // Dynamic parentId handling: if parentId is provided but is NaN or 0 (when it should be something), 
    // we might want to disable the select or handle it.
    // However, the component should just follow the 'disabled' prop and parentId.

    useEffect(() => {
        const timer = setTimeout(() => setDebouncedSearch(search), 500);
        return () => clearTimeout(timer);
    }, [search]);

    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        isLoading,
        isError
    } = useInfiniteDictionaries(type, parentId, debouncedSearch);

    // Infinite scroll observer
    useEffect(() => {
        if (!hasNextPage || isFetchingNextPage || !open) return;

        // Intersection Observer as primary method
        const observer = new IntersectionObserver(
            (entries) => {
                const first = entries[0];
                if (first.isIntersecting && hasNextPage && !isFetchingNextPage) {
                    console.log(`[DictionarySelect:${type}] Sentinel visible, fetching next page...`);
                    fetchNextPage();
                }
            },
            {
                threshold: 0,
                rootMargin: '150px' // Fetch early
            }
        );

        const currentSentinel = scrollEndRef.current;
        if (currentSentinel) {
            observer.observe(currentSentinel);
        }

        // Fallback: Scroll listener on the container
        const handleScroll = () => {
            if (!containerRef.current || isFetchingNextPage || !hasNextPage) return;

            const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
            if (scrollHeight - scrollTop - clientHeight < 100) {
                console.log(`[DictionarySelect:${type}] Scroll reached bottom (fallback), fetching...`);
                fetchNextPage();
            }
        };

        const container = containerRef.current;
        if (container) {
            container.addEventListener('scroll', handleScroll);
        }

        return () => {
            observer.disconnect();
            if (container) {
                container.removeEventListener('scroll', handleScroll);
            }
        };
    }, [hasNextPage, isFetchingNextPage, fetchNextPage, open, type]);

    const items = useMemo(() => {
        return data?.pages.flatMap((page) => page) || [];
    }, [data]);

    const selectedItem = useMemo(() => {
        if (!value) return null;
        // Try to find in current pages
        const found = items.find((item) => item.id.toString() === value);
        return found;
    }, [value, items]);

    return (
        <div className={cn("w-full transition-all duration-300", disabled && "opacity-50 cursor-not-allowed")}>
            {label && (
                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 block px-1">
                    {label} {required && <span className="text-red-500">*</span>}
                </label>
            )}
            <DropdownMenu open={open} onOpenChange={setOpen}>
                <DropdownMenuTrigger asChild>
                    <button
                        disabled={disabled}
                        type="button"
                        className={cn(
                            "flex items-center justify-between w-full px-4 h-11 sm:h-12 rounded-xl text-sm font-semibold transition-all outline-none border",
                            open
                                ? "bg-white border-slate-400 ring-2 ring-slate-100 shadow-sm"
                                : "bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50/50",
                            disabled && "bg-slate-50 border-slate-100 text-slate-400 cursor-not-allowed opacity-50"
                        )}
                    >
                        <span className={cn("truncate", !selectedItem && "text-slate-400 font-medium")}>
                            {selectedItem ? selectedItem.name : (placeholder === "Выберите..." ? t("dictionary.select") : placeholder)}
                        </span>
                        <div className="flex items-center gap-2">
                            {isLoading && <Loader2 className="h-3 w-3 animate-spin text-slate-400" />}
                            <ChevronDown className={cn("h-4 w-4 text-slate-400 shrink-0 transition-transform duration-300", open && "rotate-180")} />
                        </div>
                    </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                    align="start"
                    className="w-72 p-0 rounded-2xl shadow-2xl border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200"
                    onCloseAutoFocus={(e) => e.preventDefault()}
                >
                    <div className="p-3 bg-white border-b border-slate-50">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                            <Input
                                placeholder={t("dictionary.search")}
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                className="pl-9 h-10 bg-slate-50 border-none rounded-xl text-sm font-medium focus-visible:ring-2 focus-visible:ring-slate-100 placeholder:text-slate-400"
                                autoFocus
                            />
                        </div>
                    </div>

                    <div
                        ref={containerRef}
                        className="max-h-[300px] overflow-y-auto scrollbar-thin scrollbar-thumb-slate-200"
                    >
                        <div className="p-1.5 space-y-0.5">
                            <button
                                type="button"
                                onClick={() => {
                                    onChange(null);
                                    setOpen(false);
                                }}
                                className={cn(
                                    "w-full text-left px-3 py-2.5 rounded-lg text-sm font-semibold flex items-center justify-between transition-colors decoration-none",
                                    !value ? "bg-slate-50 text-slate-900 shadow-sm" : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                                )}
                            >
                                <span>{t("dictionary.any")}</span>
                                {!value && <Check className="h-4 w-4 text-slate-900" />}
                            </button>

                            {items.map((item) => (
                                <button
                                    key={item.id}
                                    type="button"
                                    onClick={() => {
                                        onChange(item.id.toString());
                                        setOpen(false);
                                    }}
                                    className={cn(
                                        "w-full text-left px-3 py-2.5 rounded-lg text-sm font-semibold flex items-center justify-between transition-all",
                                        value === item.id.toString()
                                            ? "bg-slate-50 text-slate-900 shadow-sm"
                                            : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                                    )}
                                >
                                    <span className="truncate">{item.name}</span>
                                    {value === item.id.toString() && <Check className="h-4 w-4 text-slate-900" />}
                                </button>
                            ))}
                        </div>

                        {isLoading && (
                            <div className="py-10 flex flex-col items-center justify-center gap-3">
                                <Loader2 className="h-6 w-6 animate-spin text-slate-300" />
                                <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest">{t("dictionary.loading")}</span>
                            </div>
                        )}

                        {isError && (
                            <div className="py-10 flex flex-col items-center justify-center gap-2 text-red-400 px-4 text-center">
                                <AlertCircle className="h-6 w-6" />
                                <span className="text-[10px] font-bold uppercase tracking-wider">{t("dictionary.error")}</span>
                            </div>
                        )}

                        {!isLoading && !isError && items.length === 0 && (
                            <div className="py-12 text-center px-4">
                                <Search className="h-8 w-8 text-slate-100 mx-auto mb-3" />
                                <div className="text-[11px] font-black text-slate-300 uppercase tracking-[0.2em]">
                                    {t("dictionary.not_found")}
                                </div>
                            </div>
                        )}

                        {/* Sensor for next page */}
                        {hasNextPage && (
                            <div ref={scrollEndRef} className="py-4 flex justify-center border-t border-slate-50 mt-2 bg-slate-50/20">
                                {isFetchingNextPage ? (
                                    <div className="flex items-center gap-2">
                                        <Loader2 className="h-4 w-4 animate-spin text-slate-400" />
                                        <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{t("dictionary.loading")}</span>
                                    </div>
                                ) : (
                                    <div className="h-2 w-full" />
                                )}
                            </div>
                        )}
                    </div>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    );
}
