from playwright.sync_api import sync_playwright
import json
import os
import requests

JSON_FILE = "incremental_graph.json"

# Get total number of pages in the wiki
def get_total_pages():
    return 37655

def get_article_links(page, article_title):
    url = f"https://oldschool.runescape.wiki/api.php?action=query&titles={article_title}&prop=links&format=json&pllimit=max"
    page.goto(url)
    body_text = page.locator("body").inner_text()
    data = json.loads(body_text)
    
    links = []
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_data in pages.items():
        if "links" in page_data:
            for link in page_data["links"]:
                links.append(link["title"])
    return links

def crawl_incremental(start_articles):
    total_pages = get_total_pages()
    print(f"Total pages in the wiki: {total_pages}")

    # Load existing JSON if it exists
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
        visited = set(graph_data.keys())
        to_visit = [a for a in start_articles if a not in visited]
    else:
        graph_data = {}
        visited = set()
        to_visit = list(start_articles)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while to_visit:
            article = to_visit.pop(0)
            if article in visited:
                continue

            print(f"Processing: {article} ({len(visited)}/{total_pages} pages read)")

            try:
                links = get_article_links(page, article)
            except Exception as e:
                print(f"Failed to fetch {article}: {e}")
                continue

            # Ensure current page exists in graph_data
            if article not in graph_data:
                graph_data[article] = {"name": article, "links_to": [], "linked_by": []}

            graph_data[article]["links_to"] = links

            # Update linked_by for linked pages
            for link in links:
                if link not in graph_data:
                    graph_data[link] = {"name": link, "links_to": [], "linked_by": []}
                if article not in graph_data[link]["linked_by"]:
                    graph_data[link]["linked_by"].append(article)
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

            visited.add(article)

            # Save JSON incrementally
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)

        browser.close()
    print(f"Finished crawling {len(visited)} pages.")

if __name__ == "__main__":
    start_articles = ["Dragon scimitar", "Dragon dagger"]
    crawl_incremental(start_articles)
