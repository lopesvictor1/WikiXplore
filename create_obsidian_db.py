import json
import os
import re
from pathlib import Path

def sanitize_filename(name):
    """
    Sanitize filename to be valid across different operating systems.
    Removes or replaces invalid characters.
    """
    # Replace invalid characters with underscore
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    
    # Limit length to avoid filesystem issues (max 255 chars for most systems)
    if len(name) > 200:
        name = name[:200]
    
    return name

def create_markdown_file(page_name, page_data, output_dir):
    """
    Create a single markdown file for a page.
    """
    safe_filename = sanitize_filename(page_name)
    filepath = output_dir / f"{safe_filename}.md"
    
    # Create markdown content
    content = f"# {page_name}\n\n"
    
    # Add links
    if page_data.get('links_to'):
        content += "## Links to\n\n"
        for link in page_data['links_to']:
            content += f"- [[{link}]]\n"
        content += "\n"
    
    # Optionally add backlinks info (just count, not actual links since Obsidian handles this)
    if page_data.get('linked_by'):
        link_count = len(page_data['linked_by'])
        content += f"---\n*This page is linked by {link_count} other pages*\n"
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def convert_json_to_obsidian(json_filepath, output_dir='WikiXplore', batch_size=100):
    """
    Convert large JSON file to Obsidian markdown files.
    Processes in batches to handle large files efficiently.
    
    Args:
        json_filepath: Path to the input JSON file
        output_dir: Directory name for the Obsidian vault
        batch_size: Number of files to process before showing progress
    """
    print(f"Starting conversion of {json_filepath}...")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    print(f"Output directory: {output_path.absolute()}")
    
    # Parse JSON - using json.load for better memory efficiency with large files
    print("Loading JSON file (this may take a moment for large files)...")
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    except MemoryError:
        print("File too large to load into memory. Consider using streaming JSON parser.")
        return
    
    # Extract graph_data
    if 'graph_data' in data:
        graph_data = data['graph_data']
    else:
        graph_data = data
    
    total_pages = len(graph_data)
    print(f"Found {total_pages} pages to convert")
    
    # Process each page
    processed = 0
    skipped = 0
    
    for page_name, page_data in graph_data.items():
        try:
            create_markdown_file(page_name, page_data, output_path)
            processed += 1
            
            # Show progress
            if processed % batch_size == 0:
                print(f"Progress: {processed}/{total_pages} pages ({(processed/total_pages)*100:.1f}%)")
        
        except Exception as e:
            print(f"Error processing '{page_name}': {e}")
            skipped += 1
    
    print("\n" + "="*50)
    print("Conversion complete!")
    print(f"✓ Successfully created: {processed} files")
    if skipped > 0:
        print(f"✗ Skipped (errors): {skipped} files")
    print(f"📁 Location: {output_path.absolute()}")
    print("="*50)
    print("\nNext steps:")
    print("1. Open Obsidian")
    print("2. Click 'Open folder as vault'")
    print(f"3. Select the '{output_dir}' folder")
    print("4. Press Ctrl+G (or Cmd+G on Mac) to open Graph View")

if __name__ == "__main__":
    # Configuration
    JSON_FILE = "incremental_graph.json"  # Change this to your JSON file path
    OUTPUT_DIR = "WikiXplore"
    
    # Check if file exists
    if not os.path.exists(JSON_FILE):
        print(f"Error: File '{JSON_FILE}' not found!")
        print("Please update the JSON_FILE variable with your actual file path.")
    else:
        convert_json_to_obsidian(JSON_FILE, OUTPUT_DIR)