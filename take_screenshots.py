"""Capture the 3 submission screenshots from a running app. Usage: python take_screenshots.py <url>"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "screenshots")
OUT.mkdir(exist_ok=True)

CASES = [
    ("positive", "Our group presentation went smoother than any rehearsal we did."),
    ("negative", "My laptop froze twice during the online quiz."),
    ("fooled", "Great, another group project where I do all the work."),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 900})
    page.goto(URL, timeout=180_000)
    # Streamlit Cloud renders the app inside an iframe at /~/+/
    root = page
    if "streamlit.app" in URL:
        page.wait_for_timeout(5000)
        root = next(f for f in page.frames if "/~/+/" in f.url)
    # cold start on the cloud can take a while
    root.get_by_text("Sentiment Analyzer").first.wait_for(timeout=180_000)
    for i, (name, text) in enumerate(CASES):
        box = root.get_by_label("Enter some text to analyze:")
        box.fill(text)
        box.press("Control+Enter")
        root.get_by_role("button", name="Analyze").click()
        # each analysis adds one row to the session history table
        root.locator("table tbody tr").nth(i).wait_for(timeout=180_000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / f"{name}.png"))
        print("saved", OUT / f"{name}.png")
    browser.close()
