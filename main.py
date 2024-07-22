from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import urllib.parse

approach = input("Choose approach (generalized/specific): ").strip().lower()
if approach == 'generalized':
    company_name = input("Enter the name of the company: ")
    formatted_name = urllib.parse.quote(company_name)
    search_url = f"https://www.linkedin.com/search/results/all/?keywords={formatted_name}"
elif approach == 'specific':
    value = input("Give URL of company: ")
    
filter_option = input(
    "Would you like to filter by location or job title? (Enter 'location' or 'job title'): ").strip().lower()
if filter_option == 'location':
    filter_value = input("Enter the location to filter by: ").strip()
elif filter_option == 'job title':
    filter_value = input("Enter the job title to filter by: ").strip()
else:
    print("Invalid filter option. Exiting.")
    exit()

id_linkedin = input("Give email of LinkedIn: ")
pass_linkedin = input("Give password of LinkedIn: ")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

filename = "linkedin_profiles.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Location', 'Profile URL'])

    try:
        driver.get("https://www.linkedin.com/login")
        username = wait.until(
            EC.visibility_of_element_located((By.NAME, "session_key")))
        password = wait.until(EC.visibility_of_element_located(
            (By.NAME, "session_password")))
        username.send_keys(id_linkedin)
        password.send_keys(pass_linkedin)
        password.send_keys(Keys.RETURN)
        wait.until(EC.element_to_be_clickable((By.ID, "global-nav-typeahead")))

        if approach == 'generalized':
            driver.get(search_url)
            time.sleep(5)
            see_all_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'See all people results')]")))
            see_all_link.click()
            time.sleep(5)
        elif approach == 'specific':
            driver.get(value)
            time.sleep(3)
            company_link = driver.find_element(
                By.CSS_SELECTOR, "span.t-normal.t-black--light.link-without-visited-state.link-without-hover-state")
            company_link.click()
            time.sleep(3)
        else:
            print("Invalid approach. Exiting.")
            exit()

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            profile_elements = soup.select(
                'div.entity-result__divider.pt3.pb3.t-12.t-black--light')

            for profile in profile_elements:
                name = profile.select_one('.app-aware-link span[aria-hidden="true"]').get_text(
                    strip=True) if profile.select_one('.app-aware-link span[aria-hidden="true"]') else 'No Name Found'
                title = profile.select_one('.entity-result__primary-subtitle').get_text(
                    strip=True) if profile.select_one('.entity-result__primary-subtitle') else 'No Title Found'
                location = profile.select_one('.entity-result__secondary-subtitle').get_text(
                    strip=True) if profile.select_one('.entity-result__secondary-subtitle') else 'No Location Found'
                profile_url = profile.select_one(
                    '.app-aware-link')['href'] if profile.select_one('.app-aware-link') else 'No URL Found'

                if filter_option == 'job title':
                    keywords = [keyword.lower() for keyword in filter_value.split()]

                if filter_option == 'location' and filter_value.lower() in location.lower():
                    writer.writerow([name, title, location, profile_url])
                elif filter_option == 'job title':
                    if any(keyword in title.lower() for keyword in keywords):
                        writer.writerow([name, title, location, profile_url])

            try:
                next_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.artdeco-pagination__button--next')))
                if next_button:
                    next_button.click()
                    time.sleep(3)
            except Exception as e:
                print("Data is fetched.")
                break

    finally:
        driver.quit()
