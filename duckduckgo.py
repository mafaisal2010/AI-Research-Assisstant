import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query, max_results=5):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__a", href=True)

        links = []
        for link in results:
            href = link['href']
            if href.startswith("http"):
                links.append(href)
            if len(links) >= max_results:
                break

        return links
    except Exception as e:
        print("DuckDuckGo search failed:", e)
        return []
