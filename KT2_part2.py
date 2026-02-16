from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

try:
    driver.get("http://www.scrapethissite.com/pages/ajax-javascript/")

    years = ["2012", "2013", "2014", "2015"]

    for year in years:
        year_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{year}']"))
        )
        year_link.click()

        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.films"))
        )

        films = []
        rows = table.find_elements(By.CSS_SELECTOR, "tr")
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue

            try:
                title = cells[0].find_element(By.TAG_NAME, "a").text.strip()
                nominations = int(cells[1].text.strip() or "0")
                wins = int(cells[2].text.strip() or "0")

                films.append({
                    "year": year,
                    "title": title,
                    "nominations": nominations,
                    "wins": wins
                })
            except:
                continue

        with open(f"{year}_films.json", "w", encoding="utf-8") as f:
            json.dump(films, f, ensure_ascii=False, indent=2)

finally:
    driver.quit()