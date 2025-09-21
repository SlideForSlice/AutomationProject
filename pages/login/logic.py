import pytest
from playwright.sync_api import Page, expect

from pages.login.locators import LoginPageLocators
from pages.my_account.locators import MyAccountPageLocators
from utils.links import Links
import allure

@allure.feature("Login Functionality")
class LoginLogic:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Login with email and password")
    @allure.severity("Critical")
    @pytest.mark.smoke
    def login(self, email: str, password: str):
        with allure.step(f"Open login page {Links.LOGIN_PAGE}"):
            self.page.goto(Links.LOGIN_PAGE, timeout=5000)
            expect(self.page.locator(LoginPageLocators.INPUT_EMAIL)).to_be_visible(timeout=5000)

            allure.attach(self.page.url, "current_url", allure.attachment_type.TEXT)

        with allure.step("Fill credentials"):
            self.page.locator(LoginPageLocators.INPUT_EMAIL).fill(email)
            self.page.locator(LoginPageLocators.INPUT_PASSWORD).fill(password)

            filled_email = self.page.locator(LoginPageLocators.INPUT_EMAIL).input_value()
            allure.attach(filled_email, "filled_email", allure.attachment_type.TEXT)

        with allure.step("Click Login"):
            self.page.locator(LoginPageLocators.BUTTON_LOGIN).click()

        with allure.step("Verify successful login (My Account visible)"):
            expect(self.page.locator(MyAccountPageLocators.TITLE_MY_ACCOUNT)).to_be_visible(timeout=20_000)
            allure.attach(self.page.url, "current_url_after_login", allure.attachment_type.TEXT)