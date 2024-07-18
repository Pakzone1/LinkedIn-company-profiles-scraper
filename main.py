from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

value = input("Give URL of company: ")
id_linkedin = input("Give email of LinkedIn: ")
pass_linkedin = input("Give password of LinkedIn: ")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

profiles = []  

try:
    driver.get("https://www.linkedin.com/login")
    username = driver.find_element(By.NAME, "session_key")
    password = driver.find_element(By.NAME, "session_password")
    username.send_keys(id_linkedin)
    password.send_keys(pass_linkedin)
    password.send_keys(Keys.RETURN)
    time.sleep(3)  

    driver.get(value)
    time.sleep(3)

    while True:
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Allow time for the page to load
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        profile_elements = soup.select('div.jNhfFQYlhemzzNBrCiOgVLjMjvsKMncxC')

        for profile in profile_elements:
            name_element = profile.select_one(
                'a.app-aware-link span[aria-hidden="true"]')
            name = name_element.get_text(
                strip=True) if name_element else 'No Name Found'

            title_element = profile.select_one(
                '.entity-result__primary-subtitle')
            title = title_element.get_text(
                strip=True) if title_element else 'No Title Found'

            location_element = profile.select_one(
                '.entity-result__secondary-subtitle')
            location = location_element.get_text(
                strip=True) if location_element else 'No Location Found'

            profile_url_element = profile.select_one('a.app-aware-link')
            profile_url = profile_url_element['href'] if profile_url_element else 'No URL Found'

            profiles.append({'name': name, 'title': title,
                            'location': location, 'profile_url': profile_url})

        next_button = driver.find_elements(
            By.CSS_SELECTOR, 'button.artdeco-pagination__button--next')
        if next_button and 'disabled' not in next_button[0].get_attribute('class'):
            next_button[0].click()
            time.sleep(3)
        else:
            break  

finally:
    driver.quit()  

filename = "linkedin_profiles.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Location', 'Profile URL'])
    for profile in profiles:
        writer.writerow([profile['name'], profile['title'],
                        profile['location'], profile['profile_url']])
