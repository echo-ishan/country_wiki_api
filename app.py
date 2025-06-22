from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(...)):
    wiki_url = f"https://en.wikipedia.org/wiki/{quote(country)}"
    try:
        response = requests.get(wiki_url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Wikipedia page not found for '{country}'")
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Error fetching Wikipedia page")

    soup = BeautifulSoup(response.content, "html.parser")
    headings = soup.select("h1, h2, h3, h4, h5, h6")

    markdown_lines = ["## Contents", ""]
    for tag in headings:
        level = int(tag.name[1])
        text = tag.get_text(strip=True)
        if text:
            markdown_lines.append("#" * level + " " + text)

    return {"outline": "\n".join(markdown_lines)}
