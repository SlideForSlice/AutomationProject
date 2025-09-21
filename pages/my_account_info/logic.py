import allure
import pytest
from playwright.sync_api import Page, expect
from utils.links import Links
from pages.my_account_info.locators import MyAccountInfoPageLocators

@allure.feature('MyAccountInfo Functionality')
class MyAccountInfoLogic:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Changing name to: {name}")
    @allure.severity("Critical")
    @pytest.mark.smoke
    def change_user_name(self, name: str):
        with allure.step(f"Open edit page"):
            self.page.goto(Links.EDIT_ACCOUNT_PAGE, timeout=30_000)
            expect(self.page.locator(MyAccountInfoPageLocators.TITLE_PAGE)).to_be_visible(timeout=15_000)
            allure.attach(self.page.url, "current_url_before_edit", allure.attachment_type.TEXT)

        with allure.step(f"Fill first name with '{name}' and verify value"):
            first_name_input = self.page.locator(MyAccountInfoPageLocators.FIRST_NAME_INPUT)
            first_name_input.fill(name)
            expect(first_name_input).to_have_value(name, timeout=10_000)
            allure.attach(first_name_input.input_value(), "first_name_input_value", allure.attachment_type.TEXT)

        with allure.step("Click 'Confirm changes'"):
            self.page.locator(MyAccountInfoPageLocators.CONFIRM_CHANGES_BUTTON).click()

        with allure.step("Verify success message is visible"):
            success = self.page.locator(MyAccountInfoPageLocators.SUCCESS_CHANGES_MESSAGE)
            expect(success).to_be_visible(timeout=15_000)
            allure.attach(self.page.url, "current_url_after_save", allure.attachment_type.TEXT)
            allure.attach(success.inner_text().strip(), "success_message_text", allure.attachment_type.TEXT)