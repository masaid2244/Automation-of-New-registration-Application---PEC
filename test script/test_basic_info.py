from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Import the page classes
from pages.base_page import BasePage
from pages.LoginPage import LoginPage
from pages.BasicInfoPage import BasicInfoPage


def test_basic_info_submission():
    # Setup Chrome WebDriver
    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service)

    try:
        # Initialize page objects
        login_page = LoginPage(driver)
        basic_info_page = BasicInfoPage(driver)

        # Perform the login
        login_page.open_login_page("http://10.0.32.90:8012/")
        login_page.login("pectesting12345@gmail.com", "pec123")
        basic_info_page.safe_click((By.ID, "wizstep1"))

        # Perform actions on the Basic Info page
        basic_info_page.select_gender("Male")
        basic_info_page.select_application_type("Graduate Before 2008")
        basic_info_page.select_blood_group("A+ve")
        time.sleep(20)
        basic_info_page.submit_basic_info()

        # Assertion
        basic_info_page.assert_basic_info_page()

    finally:
        driver.quit()
