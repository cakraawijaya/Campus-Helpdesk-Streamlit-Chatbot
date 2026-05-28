# Import Path for file system handling
from pathlib import Path

# Active custom CSS theme
# Auto-generated from THEME_MODE configuration
ACTIVE_THEME = "light_mode.css"

def load_all_css():
    # Define the folder that contains all CSS files
    css_dir = Path(__file__).parent / "styles"

    # List of CSS files that will be loaded in order
    css_files = [
        "base.css",
        ACTIVE_THEME
    ]

    # Variable to store all combined CSS content
    all_css = ""

    # Loop through each CSS file
    for file in css_files:
        # Create full file path
        path = css_dir / file

        # Check if the file exists before reading it
        if path.exists():
            # Read file content and append it to all_css
            all_css += path.read_text(encoding="utf-8") + "\n"

    # Return all combined CSS content
    return all_css