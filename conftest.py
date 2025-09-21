import os

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect

from pages.login.locators import LoginPageLocators
from pages.my_account.locators import MyAccountPageLocators
from utils.links import Links

load_dotenv()

PASSWORD = os.getenv("SITE_PASSWORD")
EMAIL = os.getenv("SITE_EMAIL")


@pytest.fixture()
def browser_set():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def logged_page(browser_set):
    page = browser_set

    page.goto(Links.LOGIN_PAGE, timeout=5000)

    expect(page.locator(LoginPageLocators.INPUT_EMAIL)).to_be_visible(timeout=5000)
    page.locator(LoginPageLocators.INPUT_EMAIL).fill(EMAIL)
    page.locator(LoginPageLocators.INPUT_PASSWORD).fill(PASSWORD)

    page.locator(LoginPageLocators.BUTTON_LOGIN).click()

    expect(page.locator(MyAccountPageLocators.TITLE_MY_ACCOUNT)).to_be_visible(timeout=5000)

    yield page

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # получаем TestReport для текущего этапа теста (setup/call/teardown)
    outcome = yield
    item.rep_call = outcome.get_result()


@pytest.fixture(autouse=True)
def _attach_on_failure(request, logged_page=None):
    # выполняем тест; после него, если он упал — прикрепляем артефакты
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = logged_page or getattr(request.node.funcargs, "logged_page", None)
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                page.content(),
                name="page_source",
                attachment_type=allure.attachment_type.HTML,
            )
