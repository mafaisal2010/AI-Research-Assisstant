import requests
import re
import wikipedia
from bs4 import BeautifulSoup

def get_wikipedia_summary_and_full_text(query):
    try:
        page = wikipedia.page(query, auto_suggest=False)
        summary = wikipedia.summary(query, auto_suggest=False)
        return summary, page.content, page.url
    except Exception as e:
        print("Wikipedia error:", e)
        return "", "", ""

def clean_wikipedia_text(text, wiki_url):
    # Remove sections like "See also", "References", etc.
    text = re.split(r"==+ *(See also|References|External links|Further reading|Notes) *==+", text, flags=re.IGNORECASE)[0]

    # Fix headers to look cleaner
    text = re.sub(r"=+ *(.*?) *=+", lambda m: f"\n\n{m.group(1).strip().upper()}\n" + "-" * len(m.group(1).strip()), text)

    # Remove citation [1], [2], etc.
    text = re.sub(r"\[\d+\]", "", text)

    # Add credit at the end
    text += f"\n\nTaken from: {wiki_url}"

    return text.strip()

def get_web_summaries(query):
    summaries = []

    try:
        # First try DuckDuckGo
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        results = soup.select(".result__snippet")[:3]
        links = soup.select(".result__url")[:3]

        for i in range(min(len(results), len(links))):
            summary = results[i].text.strip()
            link = "https://" + links[i].text.strip().lstrip("/")
            summaries.append((link, summary))
    except Exception as e:
        print("DuckDuckGo failed:", e)

    # Fallback to SerpAPI if DuckDuckGo fails
    if not summaries:
        try:
            serpapi_key = "YOUR_SERPAPI_KEY"
            url = f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}"
            res = requests.get(url)
            data = res.json()
            for result in data.get("organic_results", [])[:3]:
                link = result.get("link")
                summary = result.get("snippet", "")
                if link and summary:
                    summaries.append((link, summary))
        except Exception as e:
            print("SerpAPI failed:", e)

    return summaries
