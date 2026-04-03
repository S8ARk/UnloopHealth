from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.type} {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page error: {err}"))
        
        try:
            print("Going to login...")
            page.goto("http://localhost:8000/pages/login.html", wait_until="networkidle")
            page.fill("#email", "demo@nutricore.com")
            page.fill("#password", "password123")
            print("Clicking sign in...")
            page.click("button[type='submit']")
            page.wait_for_timeout(2000)
            print("Done")
        except Exception as e:
            print("Script err:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    test_login()
