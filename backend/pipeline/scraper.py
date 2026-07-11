# services/scraper.py
from pandas import options
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime



BASE_URL = "https://teachersnotes.pythonanywhere.com"

print("========== LOADED backend.pipeline.scraper ==========")
def format_date(date_str):
    """
    Convert YYYY-MM-DD -> (day, month, year)
    Example:
    2026-06-22 -> 22,6,2026
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.day, dt.month, dt.year

def scrape_grade(page, school, grade, from_date, to_date):

    from_day, from_month, from_year = format_date(from_date)
    to_day, to_month, to_year = format_date(to_date)

    print(f"\nOpening ShowNotes for {grade}...")

    response = page.goto(
        f"{BASE_URL}/ShowNotes",
        wait_until="networkidle",
        timeout=120000
    )
    print("\n===== COOKIES AFTER GOTO =====")
    for cookie in page.context.cookies():
        print(cookie)
    print("==============================")
    print("Status:", response.status if response else None)
    print("URL:", page.url)

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    page.wait_for_selector('select[name="School"]')

    page.select_option('select[name="School"]', school)

    print("\n===== COOKIES AFTER SCHOOL SELECT =====")
    for cookie in page.context.cookies():
        print(cookie)
    print("=======================================")
        

    page.wait_for_timeout(1000)

    page.wait_for_function("""
    () => {
        const sel = document.querySelector('select[name="Grade"]');
        return sel && sel.options.length > 1;
    }
    """)

    # -----------------------------
    # Select Grade
    # -----------------------------
    page.select_option('select[name="Grade"]', grade)

    print("\n================ BEFORE SUBMIT ================")

    print("Current URL:", page.url)
    print("Login page exists:",
      page.locator('input[name="username"]').count())

    print("Logout link:",
        page.locator('text=Logout').count())

    print("Session cookies:",
        page.context.cookies())
    print("School Value:",
          page.locator('select[name="School"]').input_value())

    print("Grade Value:",
          page.locator('select[name="Grade"]').input_value())

    print("Grade Text:",
          page.locator(
              'select[name="Grade"] option:checked'
          ).inner_text())

    options = page.locator(
        'select[name="Grade"] option'
    ).evaluate_all(
        "(opts)=>opts.map(o=>({text:o.textContent.trim(),value:o.value}))"
    )

    print("Available Grade Options:")
    for op in options:
        print(op)

    # -----------------------------
    # Dates
    # -----------------------------
    page.select_option(
        'select[name="From_date_day"]',
        str(from_day)
    )
    page.select_option(
        'select[name="From_date_month"]',
        str(from_month)
    )
    page.select_option(
        'select[name="From_date_year"]',
        str(from_year)
    )

    page.select_option(
        'select[name="To_date_day"]',
        str(to_day)
    )
    page.select_option(
        'select[name="To_date_month"]',
        str(to_month)
    )
    page.select_option(
        'select[name="To_date_year"]',
        str(to_year)
    )

    print(
        "From Date:",
        f"{from_day}/{from_month}/{from_year}"
    )

    print(
        "To Date:",
        f"{to_day}/{to_month}/{to_year}"
    )

    print("==============================================")
    print("Cookies before submit:")
    print(page.context.cookies())

    # -----------------------------
    # DEBUG SUBMIT BUTTONS
    # -----------------------------
    buttons = page.locator('button[type="submit"]')

    print("\n===== SUBMIT BUTTONS =====")
    print("Submit buttons:", buttons.count())

    for i in range(buttons.count()):
        print(f"Button {i}: '{buttons.nth(i).inner_text()}'")
    print("==========================")

    print("==============================================")
    print("Cookies before submit:")
    print(page.context.cookies())

    
    # -----------------------------
    # Submit
    # -----------------------------
    with page.expect_navigation(wait_until="load"):
        page.click('button[type="submit"]')

    # -----------------------------
    # AFTER SUBMIT
    # -----------------------------
    print("\n================ AFTER SUBMIT ================")

    print("Current URL:", page.url)
    print("Page Title:", page.title())

    # Grade dropdown
    if page.locator('select[name="Grade"]').count() > 0:
        print(
            "Grade Value:",
            page.locator('select[name="Grade"]').input_value()
        )

        print(
            "Grade Text:",
            page.locator(
                'select[name="Grade"] option:checked'
            ).inner_text()
        )
    else:
        print("Grade dropdown not found after submit.")

    # H1
    h1s = page.locator("h1")
    print("\nNumber of H1:", h1s.count())

    for i in range(h1s.count()):
        print(f"H1[{i}] = {h1s.nth(i).inner_text()}")

    # H2
    h2s = page.locator("h2")
    print("\nNumber of H2:", h2s.count())

    for i in range(h2s.count()):
        print(f"H2[{i}] = {h2s.nth(i).inner_text()}")

    # H3
    h3s = page.locator("h3")
    print("\nNumber of H3:", h3s.count())

    for i in range(h3s.count()):
        print(f"H3[{i}] = {h3s.nth(i).inner_text()}")

    # Extra page information
    print("\nButtons:", page.locator("button").count())
    print("Forms:", page.locator("form").count())
    print("Tables:", page.locator("table").count())

    # HTML Preview
    html = page.content()

    print("\n========== FIRST 1500 CHARACTERS ==========\n")
    print(html[:1500])

    print("\n===========================================")
    # -----------------------------
    # Save HTML
    # -----------------------------
    safe_grade = grade.replace("/", "_").replace(" ", "_")

    with open(
        f"debug_{safe_grade}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print(f"Saved debug_{safe_grade}.html")

    # -----------------------------
    # Parse HTML
    # -----------------------------
    soup = BeautifulSoup(html, "html.parser")
    print("\n========== VERIFY HTML ==========")
    print("Searching for Prem_M:", "Prem_M" in html)
    print("Searching for July 1:", "July 1, 2026" in html)
    print("HTML Length:", len(html))
    print("=================================")

    tables = soup.find_all("table")

    print("\n========== TABLE DEBUG ==========")
    print("Tables Found:", len(tables))

    if not tables:
        print("No tables found.")
        return []

    for i, table in enumerate(tables):

        rows = table.find_all("tr")

        print(f"\nTable {i}")
        print("Rows:", len(rows))

        if rows:
            headers = [
                x.get_text(" ", strip=True)
                for x in rows[0].find_all(["th", "td"])
            ]
            print("Headers:", headers)

    print("=================================")
    # ---------------------------------------
    # Extract teacher notes from the first table
    # ---------------------------------------

    results = []

    table = tables[0]
    rows = table.find_all("tr")

    print("Rows Found:", len(rows) - 1)

    for row in rows[1:]:      # Skip header row

        cols = row.find_all("td")

        print("--------------------------------")
        print("Columns:", len(cols))
        print([c.get_text(" ", strip=True) for c in cols])

        if len(cols) < 7:
            continue

        results.append({
            "Created_date": cols[0].get_text(" ", strip=True),
            "Username": cols[1].get_text(" ", strip=True),
            "What_I_prepared": cols[2].get_text(" ", strip=True),
            "What_I_did_well": cols[3].get_text(" ", strip=True),
            "What_went_well": cols[4].get_text(" ", strip=True),
            "Where_to_improve": cols[5].get_text(" ", strip=True),
            "What_homework_did_I_give_today": cols[6].get_text(" ", strip=True),
            "Grade": grade,
        })

    print(f"{grade} -> {len(results)} notes")

    return results


def fetch_teacher_notes(
    username,
    password,
    school,
    from_date,
    to_date
):

    all_notes = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox"
            ]
        )

        page = browser.new_page()

        page.set_default_timeout(120000)
        page.set_default_navigation_timeout(120000)

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        print("Opening login page...")
        print("Current page URL before login:", page.url)

        response = page.goto(
        f"{BASE_URL}/accounts/login/",
        wait_until="domcontentloaded",
        timeout=120000
    )

        print("Status:", response.status if response else None)
        print("URL:", page.url)

        print(
            "Username field exists:",
            page.locator('input[name="username"]').count()
        )

        print(
            "Password field exists:",
            page.locator('input[name="password"]').count()
        )

        print("Filling username...")
        print("Username:", repr(username))

        page.locator(
            'input[name="username"]'
        ).fill(username)

        print("Filling password...")
        print("Password entered.")

        page.locator(
            'input[name="password"]'
        ).fill(password)

        # -------------------------------------------------
        # CLICK LOGIN
        # -------------------------------------------------

        print("Clicking login...")

        with page.expect_navigation(wait_until="networkidle"):
            page.locator(
                'button[type="submit"], input[type="submit"]'
            ).click()
        
        print("After login URL:", page.url)
        print("Page title:", page.title())

        login_success = (
            page.locator('input[name="username"]').count() == 0
        )
        print("Cookies after login:")
        print(page.context.cookies()) 
        print("Login successful:", login_success)

        if not login_success:
            print("Login failed!")
            print(page.content()[:2000])
            browser.close()
            return []

        # -----------------------------
        # Open Show Notes page ONLY ONCE
        # -----------------------------
        page.goto(
            f"{BASE_URL}/ShowNotes",
            wait_until="load",
            timeout=120000
        )

        page.wait_for_selector(
            'select[name="School"]',
            timeout=120000
        )

        print("URL after opening ShowNotes:", page.url)
        print("Title:", page.title())

        page.wait_for_selector('select[name="School"]')

        page.select_option(
            'select[name="School"]',
            school
        )

        page.wait_for_function("""
        () => {
            const sel = document.querySelector('select[name="Grade"]');
            return sel && sel.options.length > 1;
        }
        """)

        grades = page.locator(
            'select[name="Grade"] option'
        ).all_text_contents()

        grades = [
            g.strip()
            for g in grades
            if g.strip() and g.strip().lower() not in ("select", "")
        ]

        print("Available grades:", grades)

        # -------------------------------------------------
        # SCRAPE EACH GRADE
        # -------------------------------------------------

        for grade in grades:

            print("\n===================================")
            print("Downloading Grade:", grade)
            print("===================================")

            grade_notes = scrape_grade(
                page,
                school,
                grade,
                from_date,
                to_date
            )

            print(f"\nGRADE: {grade}")
            print(f"Rows returned: {len(grade_notes)}")

            prem_found = False

            for row in grade_notes:
                print(
                    row["Username"],
                    row["Grade"],
                    row["Created_date"]
                )

                if row["Username"].strip().lower() == "prem_m":
                    prem_found = True
                    print("✅ Prem_M FOUND:", row)

            if not prem_found:
                print("❌ Prem_M NOT FOUND in this grade")

            all_notes.extend(grade_notes)

        browser.close()

    print("\n===================================")
    print("TOTAL NOTES:", len(all_notes))
    print("===================================")

    return all_notes


if __name__ == "__main__":

    notes = fetch_teacher_notes(
        username="Kayalvizhi",
        password="useme@123",
        school="Isaiambalam",
        from_date="2026-06-29",
        to_date="2026-07-04"
    )

    print(notes[:5])