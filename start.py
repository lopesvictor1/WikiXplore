import requests

url = "https://oldschool.runescape.wiki/api.php"

params = {
    "action": "query",
    "meta": "siteinfo",
    "siprop": "statistics",
    "format": "json"
}

# User-Agent precisa ser algo descritivo
headers = {
    "User-Agent": "OSRSWikiStatsBot/0.1 (victorlopesvictor@gmail.com)"
}

res = requests.get(url, params=params, headers=headers)

print("Status code:", res.status_code)
print("URL final:", res.url)

data = res.json()
total_articles = data["query"]["statistics"]["articles"]

print(f"Número total de artigos na OSRS Wiki: {total_articles}")
