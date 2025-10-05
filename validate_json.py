import json
import sys

def validate_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"✅ {filename} is a valid JSON file.")
    except json.JSONDecodeError as e:
        print(f"❌ JSONDecodeError in {filename}:")
        print(f"   {e.msg}")
        print(f"   Line: {e.lineno}, Column: {e.colno}, Char position: {e.pos}")
        print("   --- Context ---")

        # Read the file again to show the context around the error
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 2)
        for i in range(start, end):
            prefix = ">>" if i + 1 == e.lineno else "  "
            print(f"{prefix} {i+1:6d}: {lines[i].rstrip()}")

        print("\n🔎 The error is likely near the marker above.")
        print("💡 You can try truncating the file before that point or fixing missing commas/braces manually.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "incremental_graph.json"
    validate_json(filename)
