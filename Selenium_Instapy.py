from instapy import InstaPy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Get environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
target_account = os.getenv("SIMILAR_ACCOUNT")

# Initialize InstaPy
session = InstaPy(username=username, password=password)
session.login()

# Initialize Selenium WebDriver (Chrome)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
driver = webdriver.Chrome(options=chrome_options)

# Log in to Instagram using Selenium
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
password_field = driver.find_element(By.NAME, "password")

username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)
time.sleep(5)

# Navigate to the target account's followers using Selenium
driver.get(f"https://www.instagram.com/{target_account}/followers/")
time.sleep(5)

# Find and follow each follower
follow_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Follow')]")))

for button in follow_buttons:
    try:
        button.click()
        print("Followed an account.")
        time.sleep(1)  # Adjust sleep time between follows
    except Exception as e:
        print(f"Error following account: {e}")

# Close the Selenium WebDriver
driver.quit()

# End the InstaPy session
session.end()
