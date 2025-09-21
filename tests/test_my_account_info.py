import random

from playwright.sync_api import Page

from pages.my_account_info.logic import MyAccountInfoLogic


class TestMyAccountInfo:
    def test_change_user_name(self, logged_page: Page):
        page = MyAccountInfoLogic(logged_page)

        page.change_user_name(f"John {random.randint(1, 100)}")

