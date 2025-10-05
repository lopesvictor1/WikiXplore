from playwright.sync_api import sync_playwright
import json, os, time, signal, sys
from datetime import datetime

JSON_FILE = "incremental_graph.json"
SAVE_INTERVAL = 10  # Save every N pages processed

# Global stop flag
STOP_CRAWL = False

def signal_handler(sig, frame):
    global STOP_CRAWL
    print("\n[INFO] Stop signal received. Will save metadata and exit gracefully...")
    STOP_CRAWL = True

# Bind Ctrl+C to stop signal
signal.signal(signal.SIGINT, signal_handler)

def safe_load_json(filename):
    """Loads JSON safely, and returns both graph data and metadata."""
    if not os.path.exists(filename):
        print(f"[INFO] No existing file '{filename}' found. Starting fresh.")
        return {}, {
            "visited": [],
            "to_visit": [],
            "last_save": None,
            "total_pages": 0
        }

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            graph_data = data.get("graph_data", {})
            metadata = data.get("metadata", {
                "visited": [],
                "to_visit": [],
                "last_save": None,
                "total_pages": len(graph_data)
            })
            print(f"✅ Loaded {len(graph_data)} pages and metadata.")
            return graph_data, metadata

    except json.JSONDecodeError:
        print(f"[WARN] {filename} is corrupted. Attempting partial recovery...")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        last_brace = content.rfind("}")
        if last_brace == -1:
            print("[ERROR] File too broken. Starting fresh.")
            return {}, {"visited": [], "to_visit": [], "last_save": None, "total_pages": 0}

        # Try trimming content
        for cut in range(0, 5000):
            try_content = content[:last_brace - cut] + "}"
            try:
                data = json.loads(try_content)
                graph_data = data.get("graph_data", {})
                metadata = data.get("metadata", {"visited": [], "to_visit": [], "last_save": None, "total_pages": len(graph_data)})
                print(f"✅ Recovered {len(graph_data)} entries after trimming {cut} bytes.")
                return graph_data, metadata
            except:
                continue
        print("[ERROR] Could not recover. Starting fresh.")
        return {}, {"visited": [], "to_visit": [], "last_save": None, "total_pages": 0}

def save_json(graph_data, metadata):
    """Save graph and metadata to JSON."""
    metadata["last_save"] = datetime.utcnow().isoformat()
    metadata["total_pages"] = len(graph_data)
    data_to_save = {
        "graph_data": graph_data,
        "metadata": metadata
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(graph_data)} pages and metadata at {metadata['last_save']}")

def get_article_links(page, article_title):
    """Fetch article links from the wiki API using Playwright."""
    url = f"https://oldschool.runescape.wiki/api.php?action=query&titles={article_title}&prop=links&format=json&pllimit=max"
    page.goto(url)
    body_text = page.locator("body").inner_text()
    data = json.loads(body_text)
    links = []
    for _, page_data in data.get("query", {}).get("pages", {}).items():
        if "links" in page_data:
            links.extend(link["title"] for link in page_data["links"])
    return links

def crawl_incremental(start_articles):
    """Incrementally crawl and update the wiki graph with metadata, batching, and failsafe."""
    global STOP_CRAWL

    # Load existing graph and metadata
    graph_data, metadata = safe_load_json(JSON_FILE)

    visited = set(metadata.get("visited", []))
    to_visit = list(set(start_articles + metadata.get("to_visit", [])) - visited)

    print(f"[INFO] Resuming crawl with {len(visited)} visited pages and {len(to_visit)} pages to visit.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        processed_since_save = 0
        batch_visited = []

        while to_visit and not STOP_CRAWL:
            article = to_visit.pop(0)
            if article in visited:
                continue

            print(f"Processing: {article} ({len(visited)}/{len(visited) + len(to_visit)})")

            try:
                links = get_article_links(page, article)
            except Exception as e:
                print(f"❌ Failed to fetch {article}: {e}")
                # Optionally requeue the article
                to_visit.append(article)
                time.sleep(1)
                continue

            # Update graph
            if article not in graph_data:
                graph_data[article] = {"name": article, "links_to": [], "linked_by": []}
            graph_data[article]["links_to"] = links

            for link in links:
                if link not in graph_data:
                    graph_data[link] = {"name": link, "links_to": [], "linked_by": []}
                if article not in graph_data[link]["linked_by"]:
                    graph_data[link]["linked_by"].append(article)
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

            visited.add(article)
            batch_visited.append(article)
            processed_since_save += 1

            # Save batch every SAVE_INTERVAL pages
            if processed_since_save >= SAVE_INTERVAL:
                metadata["visited"].extend(batch_visited)
                metadata["to_visit"] = to_visit
                save_json(graph_data, metadata)
                processed_since_save = 0
                batch_visited = []

        # Final save when finished or stopped
        metadata["visited"].extend(batch_visited)
        metadata["to_visit"] = to_visit
        save_json(graph_data, metadata)
        browser.close()

    print(f"✅ Crawl stopped or finished. Visited {len(visited)} pages. Remaining {len(to_visit)} pages.")

if __name__ == "__main__":
    crawl_incremental(["Dragon scimitar", "Dragon dagger"])
