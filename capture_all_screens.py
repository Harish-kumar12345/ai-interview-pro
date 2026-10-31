import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PORT = 8520
BASE_URL = f"http://localhost:{PORT}"
OUT_DIR = Path(__file__).parent / "assets" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWS = [
    ("01_home_screen.png", f"{BASE_URL}/?demo=1&view=Home"),
    ("02_create_interview.png", f"{BASE_URL}/?demo=1&view=Create"),
    ("03_virtual_face_to_face_room.png", f"{BASE_URL}/?demo=1&view=Interview"),
    ("04_ai_evaluation_and_feedback.png", f"{BASE_URL}/?demo=1&view=Evaluated"),
    ("05_results_and_analytics.png", f"{BASE_URL}/?demo=1&view=Results"),
    ("06_interview_history.png", f"{BASE_URL}/?demo=1&view=History"),
]


def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{url}/_stcore/health", timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(1)
    return False


def main():
    print(f"Starting Streamlit server on port {PORT}...")
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "main.py",
            "--server.port",
            str(PORT),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=Path(__file__).parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    driver = None
    try:
        print("Waiting for Streamlit server health check...")
        if not wait_for_server(BASE_URL):
            print("ERROR: Streamlit server failed to start within timeout.")
            return

        print("Server is healthy! Initializing Headless Chrome...")
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=1366,1050")
        opts.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(1366, 1050)

        for filename, url in VIEWS:
            out_file = OUT_DIR / filename
            print(f"Capturing: {filename} from {url}...")
            driver.get(url)
            # Allow Streamlit UI and WebSockets to fully render
            time.sleep(3.5)
            driver.save_screenshot(str(out_file))
            if out_file.exists():
                print(f"[OK] Saved {filename} ({out_file.stat().st_size} bytes)")
            else:
                print(f"[FAIL] {filename}")

        print("\nAll application screenshots captured successfully!")

    finally:
        if driver:
            driver.quit()
        print("Shutting down Streamlit background process...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
