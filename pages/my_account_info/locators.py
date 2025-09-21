class MyAccountInfoPageLocators:
    FIRST_NAME_INPUT = "//input[@id='input-firstname']"
    CONFIRM_CHANGES_BUTTON = "//input[@value='Continue']"
    SUCCESS_CHANGES_MESSAGE = "//div[starts-with(normalize-space(.),'Success')]"
    TITLE_PAGE = "//h1[text()='My Account Information']"