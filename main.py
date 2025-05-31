from agent.summarizer import summarize_updates
from utils.formatter import format_newsletter
from tavily import TavilyClient
from config import TAVILY_API_KEY, OPENAI_API_KEY

from datetime import datetime, timedelta
import openai
import requests

openai.api_key = OPENAI_API_KEY

def moderate_content(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a content safety reviewer. Flag anything that is unsafe, biased, or inappropriate."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0
        )
        flagged = any(word in response.choices[0].message.content.lower() for word in ["unsafe", "bias", "inappropriate", "toxic"])
        return not flagged
    except Exception as e:
        print(f"⚠️ Error in content moderation: {e}")
        return True  # Fallback: assume safe if moderation fails

def collect_updates(topics=["AI", "Data Engineering"], fintech_companies=None):
    if fintech_companies is None:
        fintech_companies = ["Stripe", "Plaid", "Razorpay", "Wise", "Revolut", "Chime", "Brex", "Paytm"]

    client = TavilyClient(api_key=TAVILY_API_KEY)
    updates = []
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    top_ai_sources = ["medium.com", "marktechpost.com", "therundown.ai", "venturebeat.com", "huggingface.co", "openai.com", "nvidia.com", "deepmind.com", "anthropic.com", "ai.googleblog.com"]
    top_fintech_sources = ["finextra.com", "thefintechtimes.com", "paymentsdive.com", "techcrunch.com", "forbes.com/fintech", "fintechfutures.com"]

    def search_with_filters(query, category, sources, max_results=5):
        results = client.search(
            query=f"{query} after:{seven_days_ago}",
            search_depth="advanced",
            max_results=max_results,
            include_domains=sources
        )
        for r in results.get("results", []):
            if not moderate_content(r.get("content", "")):
                print(f"⚠️ Skipped unsafe content: {r.get('url')}")
                continue
            updates.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content") or "",
                "category": category
            })

    for topic in topics:
        source_list = top_ai_sources if "AI" in topic else []
        search_with_filters(topic + " trends", topic, source_list)

    for company in fintech_companies:
        search_with_filters(f"{company} fintech news", "Fintech", top_fintech_sources, max_results=3)

    return updates

def send_newsletter_email(subject, body_html, recipients):
    try:
        payload = {
            "subject": subject,
            "body_html": body_html,
            "to_emails": recipients
        }
        response = requests.post("http://127.0.0.1:5001/send-email", json=payload)
        response.raise_for_status()
        print("✅ Newsletter email sent.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling email service: {e}")

def generate_newsletter():
    updates = collect_updates()
    if not updates:
        return "⚠️ No updates found. Please try again later."

    try:
        summaries = summarize_updates(updates)
    except Exception as e:
        return f"⚠️ Error summarizing updates: {e}"

    if not isinstance(summaries, list):
        return "⚠️ Unexpected summarization output."

    newsletter_html = format_newsletter(summaries)

    # Optionally moderate the final HTML before emailing
    if not moderate_content(newsletter_html):
        return "⚠️ Newsletter content flagged as unsafe."

    # Send the email
    send_newsletter_email("📰 Weekly AI & Fintech Update", newsletter_html, ["you@example.com"])

    return "✅ Newsletter generated and sent!"
