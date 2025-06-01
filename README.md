# 🧬 BioResearch Telegram Bot

A fully automated bot that scans newly published scientific papers on **chronic pancreatitis**, filters them using an LLM (LLaMA via OpenRouter), summarizes the valuable ones in Ukrainian, and sends them to a Telegram channel or private chat.

---

## ✅ Features

- 🔍 Scrapes fresh research articles from **Europe PMC**
- 📄 Extracts full-text XML (not just abstracts)
- 🧠 Uses LLaMA (via OpenRouter API) to evaluate scientific novelty
- 🔕 Skips irrelevant or low-impact publications
- 📨 Sends only valuable summaries to **Telegram**
- ⚙️ Can run automatically via **GitHub Actions**, **cron**, or locally

---

## 🧪 Example Output

> 🧬 *Title of the Article*  
> 📅 2025-06-01  
> 🧑‍🔬 Author A, Author B  
> 📓 Journal Name  
> 🔗 [Link to Full Text](https://...)  
> 📄 Summary: ... Ukrainian short summary ...

---

## 🚀 Quickstart

1. **Clone the repo:**

```bash
git clone https://github.com/yourname/bioresearch-bot.git
cd bioresearch-bot
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Add environment variables:**

Create a `.env` file:

```
TG_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_chat_id
OPENROUTER_API_KEY=your_openrouter_api_key
```

> Don't forget to add `.env` to `.gitignore`!

4. **Run it manually:**

```bash
python main.py
```

---

## 🛠 Automation (Optional)

Use the included GitHub Actions workflow to run the bot weekly:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # every Monday at 9:00 UTC
```

Secrets to configure:

* `TG_TOKEN`
* `TG_CHAT_ID`
* `OPENROUTER_API_KEY`

---

## 📂 Project Structure

```
.
├── main.py                # Main runner script
├── scraper.py             # Europe PMC full-text article scraper
├── open_router.py         # LLM class using OpenRouter (LLaMA)
├── tg.py                  # Telegram sending class
├── .env                   # Environment variables (not committed)
└── requirements.txt       # Python dependencies
```

---

## 🧠 Model Used

By default, the bot uses:

* [`meta-llama/llama-4-scout:free`](https://openrouter.ai/models/meta-llama/llama-4-scout)
* Hosted via [OpenRouter](https://openrouter.ai)

---

Хочеш, я одразу згенерую `requirements.txt`, якщо ще не зроблено?
```
