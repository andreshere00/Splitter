import re
from pathlib import Path

readme_path = Path("README.md")
docs_index_path = Path("docs/index.md")

if not readme_path.exists():
    raise FileNotFoundError("README.md not found! Run prepare_readme.py first.")

# Read the full content of README.prepped.md
with readme_path.open("r", encoding="utf-8") as f:
    content = f.read()

# ✅ Replace ALL markdown links/images like (docs/foo/bar) → (./foo/bar)
content = re.sub(r"\((\.?/)?docs/", "(./", content)

# Add a header warning at the top
header = "<!-- ⚠️ Auto-generated from README.md. Do not edit directly. -->\n\n"
final_content = header + content

# Ensure the destination directory exists
docs_index_path.parent.mkdir(parents=True, exist_ok=True)

# Write the modified content to docs/index.md
with docs_index_path.open("w", encoding="utf-8") as f:
    f.write(final_content)

print("✅ README.md synced → docs/index.md with updated links.")
