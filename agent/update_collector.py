def collect_updates(topics=["AI", "Data Engineering"], fintech_companies=None):
    from tavily import TavilyClient
    from config import TAVILY_API_KEY

    if fintech_companies is None:
        fintech_companies = ["Stripe", "Plaid", "Razorpay", "Wise", "Revolut", "Chime", "Brex", "Paytm"]

    client = TavilyClient(api_key=TAVILY_API_KEY)
    updates = []

    # Regular topics
    for topic in topics:
        results = client.search(query=topic + " latest updates", search_depth="advanced", max_results=5)
        for r in results["results"]:
            updates.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
                "category": topic
            })

    # Fintech company-specific updates
    for company in fintech_companies:
        results = client.search(query=f"{company} latest fintech news", search_depth="advanced", max_results=3)
        for r in results["results"]:
            updates.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
                "category": "Fintech"
            })

    return updates
