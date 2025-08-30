import httpx

async def fetch_github_trending(topic: str):
    url = f"https://api.github.com/search/repositories?q={topic}&sort=stars&order=desc&per_page=3"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            data = r.json().get("items", [])
            return [f"🌟 {repo['name']} - {repo['html_url']}" for repo in data]
    return ["⚠️ No trending GitHub repos found."]

async def fetch_medium_articles(topic: str):
    url = f"https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/tag/{topic}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            data = r.json().get("items", [])
            return [f"📝 {a['title']} - {a['link']}" for a in data[:3]]
    return ["⚠️ No Medium articles found."]
