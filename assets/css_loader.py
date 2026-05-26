from pathlib import Path

def load_all_css():
    css_dir = Path("styles")

    css_files = [
        "base.css",
        "light_mode.css",
        "dark_mode.css"
    ]

    all_css = ""

    for file in css_files:
        path = css_dir / file
        if path.exists():
            all_css += path.read_text() + "\n"

    return all_css