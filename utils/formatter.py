def format_newsletter(summaries):
    newsletter = "# Weekly AI, Data & Fintech Updates\n\n"
    
    known_categories = {"AI", "Data Engineering", "Fintech", "Other"}
    categories = {cat: [] for cat in known_categories}

    # Categorize items
    for item in summaries:
        raw_cat = item.get("category", "").strip().lower()
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()

        if not raw_cat:
            if "ai" in text or "artificial intelligence" in text:
                cat = "AI"
            elif "data engineering" in text or "data pipeline" in text:
                cat = "Data Engineering"
            elif "fintech" in text or "finance" in text:
                cat = "Fintech"
            else:
                cat = "Other"
        else:
            if "ai" in raw_cat:
                cat = "AI"
            elif "data" in raw_cat and "engineer" in raw_cat:
                cat = "Data Engineering"
            elif "fintech" in raw_cat or "finance" in raw_cat:
                cat = "Fintech"
            else:
                cat = "Other"

        categories[cat].append(item)

    # Format each category, limiting to 5 items
    for cat in known_categories:
        items = categories.get(cat, [])
        if not items:
            continue

        newsletter += f"## 🔹 {cat} Updates\n\n"
        for i in items[:8]:
            title = i.get("title", "Untitled")
            summary = i.get("summary", i.get("content", "")).strip()
            url = i.get("url", "#")
            newsletter += f"### {title}\n\n{summary}\n\n[Read more]({url})\n\n"

        newsletter += "---\n"

    return newsletter
