from instapy import InstaPy
from instapy import smart_run
import os
from dotenv import load_dotenv
"""Consider using libraries specifically designed for Instagram automation like Instapy or Selenium InstaPy.  These 
libraries often stay updated with Instagram changes and provide functionalities for following accounts.

Or API for better stability"""
# Load environment variables from .env file
load_dotenv("./vars/.env")

# Instagram credentials
insta_username = os.getenv("USERNAME")
insta_password = os.getenv("PASSWORD")

# Target account to follow its followers
target_account = os.getenv("SIMILAR_ACCOUNT")

# Initialise InstaPy session
session = InstaPy(username=insta_username, password=insta_password, headless_browser=False)

# Login to Instagram
with smart_run(session):
    session.login()

    # Interact with the target account's followers
    session.set_relationship_bounds(enabled=True, max_followers=200)
    session.set_skip_users(skip_private=False, private_percentage=100, skip_no_profile_pic=True, no_profile_pic_percentage=100)

    # Follow the followers of the target account
    session.follow_user_followers([target_account], amount=3, randomize=True)

# End the session
session.end()
