from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from the .env file
load_dotenv("./vars/.env")

YOUR_EMAIL = os.getenv("USERNAME")
YOUR_PASSWORD = os.getenv("PASSWORD")
SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")


class InstaFollower:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.accounts_to_follow = []

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")

        try:
            email_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
            email_box.send_keys(YOUR_EMAIL)

            password_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
            password_box.send_keys(YOUR_PASSWORD)

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            submit_button.click()

            time.sleep(8)  # Adjust sleep time as needed to ensure login is complete

            # No need to waste time dismissing those 2 pop-up (issue with XPATH)
            # This is because you can perform find_follower() right away

        except Exception as e:
            print(f"Error during login: {e}")

    def find_followers(self, target_account):
        try:
            self.driver.get(f"https://www.instagram.com/{target_account}/")
            time.sleep(5)

            # Click on the Followers button to trigger the pop-up
            followers_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/followers/')]")))
            followers_button.click()

            # Wait for the followers list to load in the pop-up
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//ul")))

            # Get all follow buttons using the specific XPath provided
            follow_buttons = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div/div/div[3]/div/button")

            print(f"Located {len(follow_buttons)} followable accounts.")

            # Remove already followed or requested accounts
            self.accounts_to_follow = [account for account in follow_buttons if not self.is_followed(account)]

        except Exception as e:
            print(f"Error finding followers: {e}")

    def is_followed(self, account):
        try:
            status = account.text.strip()
            return status in ["Requested", "Following"]
        except Exception as e:
            print(f"Error checking follow status: {e}")
            return False

    def follow(self):
        try:
            for account in self.accounts_to_follow[:3]:  # Limit to 3 accounts to follow
                try:
                    # Scroll into view before clicking to ensure it's clickable
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", account)
                    time.sleep(1)  # Let it settle
                    account.click()
                    print("Follow confirmed.")
                    time.sleep(1)  # Adjust sleep time between follows
                except Exception as e:
                    print(f"Error following account: {e}")

            print("Successfully followed accounts. Quitting browser in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"Error following accounts: {e}")
        finally:
            self.driver.close()


if __name__ == "__main__":
    bot = InstaFollower()
    bot.login()
    bot.find_followers(SIMILAR_ACCOUNT)
    bot.follow()
