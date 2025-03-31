import re
import subprocess
from pathlib import Path

readme_path = Path("README.md")

if not readme_path.exists():
    raise FileNotFoundError("README.md not found!")

# Read the full content of README.md
with readme_path.open("r", encoding="utf-8") as f:
    content = f.read()

# Define a regex pattern to match the previously appended block,
# which starts with "----" then "## Project Structure", and continues until the end of the 
# contact section.
pattern = (
    r"\n----\n\n## Project Structure\n\n```sh\n.*?\n```\n\n"
    r"----\n\n## Contact Information\n\n"
    r"- E-mail: \[andresherencia2000@gmail\.com\]\(mailto:andresherencia2000@gmail\.com\)\.\n"
    r"- LinkedIn: \[link\]\(https://linkedin\.com/in/andres-herencia\)\."
)

# Remove the block if it exists
content = re.sub(pattern, "", content, flags=re.DOTALL)

# Run the 'tree' command to get the project structure
try:
    tree_output = subprocess.check_output(["tree"], encoding="utf-8")
except Exception as e:
    tree_output = f"Error running tree command: {e}"

# Prepare the new appended information
append_info = f"""

----

## Project Structure

```sh
{tree_output}
```

----

## Contact Information

- E-mail: [andresherencia2000@gmail.com](mailto:andresherencia2000@gmail.com).
- LinkedIn: [link](https://linkedin.com/in/andres-herencia).
"""

content += append_info

with readme_path.open("w", encoding="utf-8") as f: 
    f.write(content)

print("✅ README.md updated with current project structure.")
