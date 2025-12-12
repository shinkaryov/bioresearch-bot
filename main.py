from tg import TelegramNotifier
from open_router import LLMOpenRouter
from scraper import EuropePMCScraper

LLM_TEXT_CHAR_LIMIT = 15_000

scraper = EuropePMCScraper(days_back=120)
articles = scraper.get_recent_articles()


notifier = TelegramNotifier()
llm = LLMOpenRouter()

for article in articles:
    text = article.get("text", "")
    if not text:
        continue

    if len(text) > LLM_TEXT_CHAR_LIMIT:
        text = text[:LLM_TEXT_CHAR_LIMIT]

    try:
        summary = llm.summarize(title=article["title"], abstract=text)
    except Exception as e:
        print(f"⚠️ LLM помилка: {e}")
        continue

    if summary.strip().startswith("❌"):
        print(f"🔕 Стаття відхилена: {article['title']}")
        continue

    message = (
        f"🧬 *{article['title']}*\n"
        f"📅 {article['date']}\n"
        f"🧑‍🔬 {article['authors']}\n"
        f"📓 {article['journal']}\n"
        f"🔗 {article['link']}\n\n"
        f"📄 {summary}"
    )

    try:
        notifier.send_message(message)
        print(f"✅ Відправлено: {article['title']}")
    except Exception as e:
        print(f"❌ Telegram помилка: {e}")
