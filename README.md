Given below is the guide to use this scraper:

Requirements

•	Python Installation: Ensure Python is installed on your system.

•	Libraries Installation: Install Selenium, BeautifulSoup, and WebDriver Manager by running:
		pip install selenium beautifulsoup4 webdriver-manager

Script Overview

•	This script automates LinkedIn profile scraping based on company-specific or generalized search queries. Users can refine results by location or job title. The profiles are then saved into a CSV file.

Setup

•	WebDriver: The script uses ChromeDriver managed by WebDriver Manager, which simplifies the driver management automatically.

•	Credentials: LinkedIn login credentials are required for authentication.

Step-by-Step Guide

Step 1: Choose Search Approach

•	Run the script. It prompts you to choose between a 'generalized' search(by company name) or a 'specific' search(by company URL).

Step 2: Input Search Details

•	For the 'generalized' approach, input the company's name.

•	For the 'specific' approach, provide the exact LinkedIn URL of the company.

Step 3: Filtering Options

•	Choose to filter the search results by either 'location' or 'job title'. Input the respective filter details when prompted.

Step 4: LinkedIn Authentication

•	Enter your LinkedIn email and password. These credentials are used to log in to LinkedIn via the automated browser.

Step 5: Data Scraping

•	The script navigates through LinkedIn, performing searches based on the provided criteria.

•	It scrolls through the search results, extracts relevant data(name, job title, location, profile URL), and checks if they match the given filters.

Step 6: Saving Data

•	Extracted profiles that match the filters are written into a CSV file named linkedin_profiles.csv.

•	Each profile's details are saved as a row containing the person's name, title, location, and LinkedIn profile URL.

Step 7: Termination

•	Once there are no more pages to scrape or an error occurs, the script will stop.

•	The Chrome browser session is safely closed using driver.quit().

Handling Exceptions

•	The script includes error handling for situations like missing next page buttons, indicating the end of available search results.

•	Error messages and prompts guide you through the process or exit the script if invalid inputs are detected.

Notes

•	LinkedIn's Policies: Be aware of LinkedIn's terms of service, which may restrict automated data scraping activities.

•	Script Efficiency: The script includes deliberate delays(time.sleep()) to mimic human interaction and prevent quick, repetitive requests that could lead to being blocked by
LinkedIn.


@copyright
Code by Shahbaz
