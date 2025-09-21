from playwright.sync_api import Page
import os
from dotenv import load_dotenv
from pages.login.logic import LoginLogic

load_dotenv()

PASSWORD = os.getenv("SITE_PASSWORD")
EMAIL = os.getenv("SITE_EMAIL")

class TestLogin:

    def test_access_my_account(self, browser_set: Page):
        page = LoginLogic(browser_set)

        page.login(EMAIL, PASSWORD)



