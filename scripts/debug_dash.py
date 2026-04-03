from playwright.sync_api import sync_playwright
import time

def test_login_and_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        exceptions = []
        logs = []
        
        page.on("console", lambda msg: logs.append(f"LOG: {msg.type} {msg.text}"))
        page.on("pageerror", lambda err: exceptions.append(f"ERR: {err}"))
        
        try:
            print("Registering new user...")
            email = f"test_{int(time.time())}@nutri.com"
            page.goto("http://localhost:8000/pages/register.html")
            page.fill("#name", "Dash Test")
            page.fill("#email", email)
            page.fill("#password", "password123")
            page.fill("#confirmPassword", "password123")
            page.fill("#age", "30")
            page.fill("#weight", "70")
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button[type='submit']")
            page.wait_for_timeout(1000)
            
            print("Logging in...")
            page.goto("http://localhost:8000/pages/login.html")
            page.fill("#email", email)
            page.fill("#password", "password123")
            page.click("button[type='submit']")
            page.wait_for_timeout(1000)
            
            print("In Dashboard, filling Profile...")
            page.goto("http://localhost:8000/pages/profile.html")
            page.fill("input[name='age']", "30")
            page.select_option("select[name='gender']", "Male")
            page.fill("input[name='height_cm']", "180")
            page.fill("input[name='weight_kg']", "80")
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("button[type='submit']")
            page.wait_for_timeout(1000)
            
            print("Back to dashboard... waiting 3 seconds")
            page.goto("http://localhost:8000/pages/dashboard.html")
            page.wait_for_timeout(3000)
            
            print("--- LOGS ---")
            for l in logs: print(l)
            print("--- UNHANDLED ERRORS ---")
            for e in exceptions: print(e)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_login_and_dashboard()
