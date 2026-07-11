from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://teachersnotes.pythonanywhere.com/accounts/login/")

    page.locator('input[name="username"]').fill("Kayalvizhi")
    page.locator('input[name="password"]').fill("useme@123")

    print("Success")

    browser.close()