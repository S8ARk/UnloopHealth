from playwright.sync_api import sync_playwright
import time
import sys

def test_full_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.type} {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page error: {err}"))
        
        email = f"test_e2e_{int(time.time())}@nutricore.com"
        
        try:
            print("Going to register...")
            page.goto("http://localhost:8000/pages/register.html", wait_until="networkidle")
            page.fill("#name", "Test User")
            page.fill("#email", email)
            page.fill("#password", "password123")
            page.fill("#confirmPassword", "password123")
            page.fill("#age", "30")
            page.fill("#weight", "75")
            print("Clicking Register...")
            
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button[type='submit']")
            page.wait_for_timeout(2000)
            
            print(f"Current URL after register: {page.url}")
            
            # Now Login
            page.fill("#email", email)
            page.fill("#password", "password123")
            page.click("button[type='submit']")
            page.wait_for_timeout(2000)
            
            print(f"Current URL after login: {page.url}")
            
            # Check Dashboard
            score = page.locator("#overallScore").inner_text()
            print(f"Loaded Risk Score on Dashboard: {score}")
            
        except Exception as e:
            print("Script err:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    test_full_flow()
