from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import feedparser

app = FastAPI()
templates = Jinja2Templates(directory=".")

@app.get("/fetch_blogs/")
def fetch_latest_blogs(request: Request, username: str, count: int = 5):
    feed_url = f"https://medium.com/feed/@{username}"
    feed = feedparser.parse(feed_url)

    blogs = []
    for entry in feed.entries[:count]:
        image_url = "https://via.placeholder.com/300"
        if "media_content" in entry and entry.media_content:
            image_url = entry.media_content[0]["url"]
        elif "content" in entry:
            import re
            match = re.search(r'<img[^>]+src="([^">]+)"', entry.content[0].value)
            if match:
                image_url = match.group(1)

        blogs.append({
            "title": entry.title,
            "link": entry.link,
            "image": image_url,
            "summary": entry.summary[:100]
        })

    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})
