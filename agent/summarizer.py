from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_updates(updates):
    summaries = []
    for item in updates:
        try:
            prompt = f"Summarize this news article in 2 sentences:\n\nTitle: {item['title']}\n\nContent: {item['content']}"
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = "⚠️ Summary not available due to an error."
            print(f"Error summarizing: {item['title']} → {e}")

        summaries.append({
            "title": item["title"],
            "url": item["url"],
            "summary": summary,
            "category": item.get("category", "Other")
        })
    return summaries

