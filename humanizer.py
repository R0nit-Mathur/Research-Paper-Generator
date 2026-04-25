import subprocess
import time
import os
from playwright.sync_api import sync_playwright

os.environ["NODE_NO_WARNINGS"] = "1"

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
DEBUG_PORT = "9222"
GPTINF_URL = "https://gptinf.com/"


def close_brave():
    os.system("taskkill /F /IM brave.exe >nul 2>&1")
    time.sleep(2)


def launch_brave():
    subprocess.Popen([
        BRAVE_PATH,
        "--incognito",
        f"--remote-debugging-port={DEBUG_PORT}",
        "--user-data-dir=C:\\temp\\brave-debug"
    ])
    time.sleep(6)


def humanize_chunk(chunk):

    launch_brave()

    with sync_playwright() as p:

        browser = p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
        context = browser.contexts[0]

        page = context.pages[0]

        page.goto(GPTINF_URL, wait_until="networkidle")

        page.wait_for_selector("textarea.editor-textarea", timeout=60000)

        page.locator("textarea.editor-textarea").fill(chunk)

        page.locator("[data-humanize-button='humanize-button']").click()

        page.wait_for_selector(
            "textarea[data-rich-textarea='true']",
            timeout=120000
        )

        output = page.locator(
            "textarea[data-rich-textarea='true']"
        ).input_value()

    close_brave()

    return output


def humanize_chunks(chunks, output_file="output.txt"):

    # clear previous output
    open(output_file, "w").close()

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks, 1):

        print(f"Processing chunk {i}/{len(chunks)}")

        try:
            output = humanize_chunk(chunk)

        except Exception as e:
            print("Chunk failed:", e)
            output = chunk

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(output + "\n\n")

    print("Finished. All chunks saved to", output_file)