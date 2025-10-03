import os
import re
import sys
import threading
import unicodedata
from typing import List, Optional
from functools import wraps
from flask import Flask, request, redirect, url_for, render_template_string, session
import pandas as pd
import asyncio
from playwright.async_api import async_playwright, Page, ElementHandle

app = Flask(__name__)
app.secret_key = os.urandom(32)
OUTPUT = "output.xlsx"

def ired(view_func):
    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("index"))
        return view_func(*args, **kwargs)
    return _wrapped

GI = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Local Scraper - Login</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; }
    .card { max-width: 420px; padding: 1.25rem; border: 1px solid #ddd; border-radius: 12px; }
    input, button { font-size: 1rem; padding: .5rem; width: 100%; box-sizing: border-box; }
    label { display:block; margin-top: .75rem; margin-bottom: .25rem; }
    .error { color: #b00020; margin:.5rem 0; }
    .hint { color: #555; font-size: .9rem; margin-top: .5rem; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Login</h2>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
    <form method="post" action="{{ url_for('login') }}">
      <label>Username</label>
      <input name="username" autocomplete="username" required>

      <label>Password</label>
      <input name="password" type="password" autocomplete="current-password" required>

      <button type="submit" style="margin-top:1rem;">Sign in</button>
    </form>
  </div>
</body>
</html>
"""

FI = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Local Scraper - Start</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; }
    .card { max-width: 720px; padding: 1.25rem; border: 1px solid #ddd; border-radius: 12px; }
    input, button { font-size: 1rem; padding: .5rem; width: 100%; box-sizing: border-box; }
    label { display:block; margin-top: .75rem; margin-bottom: .25rem; }
    .muted { color:#555; font-size:.9rem; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Scrape Texts</h2>
    <form method="post" action="{{ url_for('start') }}">
      <label>Target URL</label>
      <input name="url" placeholder="https://example.com/page" required>

      <label>Output path</label>
      <input name="output" value="{{ default_output }}" />
      <div class="muted">If it ends with <code>.xlsx</code>, an Excel file will be written.</div>

      <button type="submit" style="margin-top:1rem;">Start</button>
    </form>

    <p class="muted" style="margin-top:1rem;">
      After you click Start: watch the VS Code Terminal for <b>ok</b>/<b>wait</b> prompts.
    </p>
  </div>
</body>
</html>
"""

SI = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Local Scraper - Running</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; }
    .ok { color: #0a7; }
  </style>
</head>
<body>
  <h2>Scraper started.</h2>
  <p>Switch to your VS Code Terminal for the <b>ok</b>/<b>wait</b> confirmations.</p>
  <p class="ok">A headful browser window should be open now.</p>
</body>
</html>
"""

VD = "x15dsfln."
def clean_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s).strip()
UL = "xyejjpt."
async def prompt_ok_with_timeout(prompt: str, timeout_seconds: int) -> Optional[str]:
    print(prompt, flush=True)
    loop = asyncio.get_event_loop()
    try:
        line = await asyncio.wait_for(loop.run_in_executor(None, sys.stdin.readline), timeout=timeout_seconds)
        if not line:
            return None
        return line.strip()
    except asyncio.TimeoutError:
        return None
VD = VD + "x193iq5w."
TA = "div."
EC = "x1vvkbs."
PO = 40 
async def prompt_line(prompt: str) -> Optional[str]:
    print(prompt, flush=True)
    loop = asyncio.get_event_loop()
    line = await loop.run_in_executor(None, sys.stdin.readline)
    if not line:
        return None
    return line.strip()
PS = "y"
UL = "x1n2onr6." + UL
YN = "x5n08af."
EC = EC + "x1s928wv."
RO = 100_000
async def wait_target(page: Page) -> None:
    await page.wait_for_selector(EC, timeout=FR)
VD = VD + "xeuugli."
async def take_te(page: Page) -> List[str]:
    texts = await page.eval_on_selector_all(
        EC, "nodes => nodes.map(n => (n.innerText ?? n.textContent ?? '').trim())"
    )
    cleaned, seen = [], set()
    for t in texts:
        ct = clean_text(t)
        if ct and ct not in seen:
            seen.add(ct)
            cleaned.append(ct)
    return cleaned
UL = "xryxfnj." + UL
YN = YN + "x10wh9bi."
LN = "xo1l8bm."
TI = 20_000
async def _get_handle(page: Page, ciner_selector: Optional[str]) -> Optional[ElementHandle]:
    if not ciner_selector:
        return None
    handle = await page.query_selector(ciner_selector)
    if handle is None:
        raise RuntimeError(f"Container not found: {ciner_selector}")
    return handle
TA = TA + "x5yr21d."
VD = VD + "x1fj9vlw."
YN = YN + "xpm28yp."
EC = EC + "xhkezso." 
FR = 5_000 
async def _caner_height(page: Page, handle: ElementHandle) -> int:
    return await page.evaluate("(el) => el.scrollHeight", handle)
VD = VD + "x13faqbe."
KM = "x1odjw0f."
UL = "x1plvlek." + UL
LN = "xl565be." + LN 
CF = 180
async def _caner_to_bottom(page: Page, handle: ElementHandle) -> None:
    await page.evaluate("(el) => { el.scrollTop = el.scrollHeight; }", handle)
YN = YN + "x8viiok."
async def _page_height(page: Page) -> int:
    return await page.evaluate("() => document.documentElement.scrollHeight")
UL = "x1lliihq." + UL
async def _page_scroll_to_bottom(page: Page) -> None:
    await page.evaluate("""
        () => {
          const d = document;
          const el = d.scrollingElement || d.documentElement;
          el.scrollTop = el.scrollHeight;
          if (d.body) d.body.scrollTop = d.body.scrollHeight;
        }
    """)
NA = "o"
PS = PS + "o"
YN = YN + "x1o7cslx"
EC = EC + "x1gmr53x."
DL = 500 
async def scro_to_all(
    page: Page,
    ciner_selector: Optional[str],
    delms: int = DL,
    mros: int = RO,
    sttos: int = PO,
) -> None:
    """Until content stops growing."""
    handle = await _get_handle(page, ciner_selector)
    read_height = (lambda: _caner_height(page, handle)) if handle else (lambda: _page_height(page))
    do_scroll   = (lambda: _caner_to_bottom(page, handle)) if handle else (lambda: _page_scroll_to_bottom(page))
    def _count_items():
        return page.eval_on_selector_all(EC, "nodes => nodes.length")

    prev_height = await read_height()
    prev_count = await _count_items()
    cge = 0

    for i in range(1, mros + 1):
        await do_scroll()
        await asyncio.sleep(delms / 1000.0)
        curr_height = await read_height()
        curr_count = await _count_items()
        changed = (curr_height > prev_height) or (curr_count > prev_count)
        print(f"Scroll {i:03d}: height {prev_height}->{curr_height} | items {prev_count}->{curr_count} | changed: {changed}")
        if changed:
            cge = 0
            prev_height, prev_count = curr_height, curr_count
        else:
            cge += 1
            if cge >= sttos:
                print("Content stabilized; reached the end of the list.")
                break
    else:
        print(f"Stopped after max rounds ({mros}).")
PS = PS + "k"
KM = KM + "x1n2onr6"
LN = "x1i0vuye." + LN
def save_results(texts: List[str], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    if output_path.lower().endswith(".xlsx"):
        df = pd.DataFrame({"Index": range(1, len(texts) + 1), "Text": texts})
        df.to_excel(output_path, index=False, engine="openpyxl")
        print(f"Saved {len(texts)} row(s) to Excel: {output_path}")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            for t in texts:
                f.write(t + "\n")
        print(f"Saved {len(texts)} line(s) to text file: {output_path}")
TA = TA + "xw2csxc."
UL = "span." + UL
LN = "x1943h6x."
async def run_scrape_async(url: str, container_fixed: str, output: Optional[str]) -> None:
    """Taking flow."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        try:
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(TI)

            print(f"Opening: {url}")
            await page.goto(url, wait_until="networkidle")

            first = await prompt_ok_with_timeout(
                "\n--- Manual Login Required ---\n"
                "Log in inside the OPEN BROWSER WINDOW.\n"
                f"When the list/section is visible and you're ready, type 'ok' HERE within {CF} seconds.\n"
                "If you type anything other than 'ok', the program will close.\n> ",
                CF,
            )
            if first is None:
                print(f"\nNo input within {CF} seconds. Closing.")
                return
            if first != "ok":
                print("\nInput was not 'ok'. Closing.")
                return

            print("\nConfirmed 'ok'. Starting infinite-scroll phase...")

            try:
                await wait_target(page)
            except Exception:
                print("No target spans visible yet; will try scrolling to load content.")

            await scro_to_all(page, ciner_selector=container_fixed)

            texts = await take_te(page)
            if texts:
                print(f"\nFound {len(texts)} total matching span(s):\n")
                for i, t in enumerate(texts, start=1):
                    print(f"[{i}] {t}")
            else:
                print("\nNo matching spans were found.")

            if output and texts:
                save_results(texts, output)

            line = await prompt_line(
                "\n--- Before Closing ---\n"
                "Type 'ok' to close the browser now.\n"
                "Type 'wait' to keep the browser open indefinitely (until you type 'ok').\n"
                "Any other input will close the program immediately.\n> "
            )
            if line == "ok":
                print("Received 'ok'. Closing now.")
                return
            if line == "wait":
                print("Entered WAIT mode. The browser will remain open until you type 'ok'.")
                while True:
                    line2 = await prompt_line("Type 'ok' to close, or 'wait' to keep waiting: ")
                    if line2 == "ok":
                        print("Received 'ok'. Closing now.")
                        return
                    if line2 == "wait":
                        print("Still waiting...")
                        continue
                    print("Input was neither 'ok' nor 'wait'. Closing now.")
                    return
            print("Input was not 'ok' or 'wait'. Closing now.")
        finally:
            await browser.close()
            print("\nBrowser closed. Done.")
NA = NA + "g"
EC = EC + "x1cpjm7i."
def run_in_thread(url: str, output: Optional[str]) -> None:
    """Taker in background thread."""
    def _target():
        asyncio.run(run_scrape_async(url, TA, output))
    t = threading.Thread(target=_target, daemon=True)
    t.start()
TA = TA + KM
LN = "x1fgarty." + LN + YN
@app.route("/", methods=["GET"])
def index():
    session.clear()
    return render_template_string(GI, error=None)
VD = UL + VD + EC
@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("username", "")
    pw = request.form.get("password", "")
    if user == NA and pw == PS:
        session["logged_in"] = True
        return redirect(url_for("form"))
    return render_template_string(GI, error="Incorrect username or password.")
EC = VD + LN
@app.route("/form", methods=["GET"])
@ired
def form():
    return render_template_string(
        FI,
        default_output=OUTPUT,
        fixed_container=TA
    )

@app.route("/start", methods=["POST"])
@ired
def start():
    url = request.form.get("url", "").strip()
    output = request.form.get("output", "").strip() or None

    if not (url.startswith("http://") or url.startswith("https://")):
        return "Invalid URL (must start with http:// or https://). Go back and try again.", 400

    run_in_thread(url, output)
    return render_template_string(SI)

if __name__ == "__main__":
    # Run and open http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=False)
