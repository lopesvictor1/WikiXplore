# OSRS WikiXplore Project

This project is designed to crawl the Old School RuneScape (OSRS) Wiki, extract relationships between pages, and create a navigable graph of content. It also supports visualization using Neo4j or Obsidian.

## Features

* Incremental crawling of OSRS Wiki articles using Playwright.
* Resume-safe crawling with metadata and batching.
* Handles corrupted JSON files and allows partial recovery.
* Batch saving of visited pages to reduce memory overhead.
* Graceful stop using Ctrl+C with automatic metadata persistence.
* Supports graph visualization via Neo4j or Obsidian.

## Files

### `start.py`

The main crawler that:

* Incrementally crawls the wiki starting from a set of articles.
* Tracks visited pages and pages to visit.
* Saves the graph and metadata periodically.
* Handles stop signals gracefully.

### `create_obsidian_db.py`

* Reads the JSON graph and generates Markdown (`.md`) files for each page.
* Enables using Obsidian to visualize page relationships.
* Each page is saved as a separate Markdown file in a `WikiXplore` folder.

### `create_neo4j_cyper.py`

* Converts the JSON graph into Neo4j Cypher statements.
* Enables visualization and exploration of the graph in Neo4j.

## Metadata Handling

* JSON now includes both the graph data and metadata.
* Metadata tracks:

  * `visited`: list of already crawled pages.
  * `to_visit`: list of pages queued for crawling.
  * `last_save`: timestamp of the last save.
  * `total_pages`: current count of pages in the graph.
* Metadata is updated every `SAVE_INTERVAL` pages.

## Important Notes

* Large graphs (~300MB) are handled carefully with batching.
* API pagination (`plcontinue`) is used to ensure all links from a page are captured.
* Only namespace 0 (main articles) is crawled by default; full wiki crawling requires iterating over all namespaces.
* Ctrl+C triggers a graceful stop that saves the current state.

## Usage

1. Start the crawler:

```bash
python3 start.py
```

2. Generate Obsidian Markdown files:

```bash
python3 create_obsidian_db.py
```

3. Generate Neo4j Cypher import file:

```bash
python3 create_neo4j_cyper.py
```

4. Use Obsidian to explore pages or Neo4j to visualize the graph.

## Future Improvements

* Optional crawling of all namespaces to capture the full 492,126 pages.
* Compressed JSON storage for faster I/O and reduced disk usage.
* More advanced metadata reporting and batch recovery for very large datasets.

---

This project is a work in progress, aiming to create a complete, navigable graph of the OSRS Wiki for analysis and visualization.
