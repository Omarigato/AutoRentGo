export default function AboutPage() {
    return (
        <div className="container max-w-4xl py-16">
            <h1 className="text-4xl font-black mb-8">О нас</h1>

            <div className="prose prose-slate max-w-none space-y-6">
                <p className="text-lg text-slate-600">
                    AutoRentGo — это современная платформа для продажи и покупки автомобилей в Казахстане.
                    Мы создали удобный сервис, который помогает тысячам людей найти автомобиль своей мечты.
                </p>

                <h2 className="text-2xl font-bold mt-8 mb-4">Наша миссия</h2>
                <p className="text-slate-600">
                    Сделать процесс покупки и продажи автомобилей простым, безопасным и прозрачным.
                    Мы стремимся обеспечить лучший пользовательский опыт и качественный сервис для всех наших клиентов.
                </p>

                <h2 className="text-2xl font-bold mt-8 mb-4">Почему выбирают нас?</h2>
                <ul className="list-disc list-inside space-y-2 text-slate-600">
                    <li>Проверенные объявления</li>
                    <li>Удобный поиск и фильтры</li>
                    <li>Безопасные сделки</li>
                    <li>Поддержка 24/7</li>
                    <li>Широкий выбор автомобилей</li>
                </ul>

                <h2 className="text-2xl font-bold mt-8 mb-4">Контакты</h2>
                <p className="text-slate-600">
                    Если у вас есть вопросы или предложения, свяжитесь с нами:
                </p>
                <ul className="list-none space-y-2 text-slate-600">
                    <li>📞 Телефон: +7 (777) 123-45-67</li>
                    <li>📧 Email: support@autorentgo.kz</li>
                    <li>📍 Адрес: г. Алматы, пр. Абая 150</li>
                </ul>
            </div>
        </div>
    );
}
