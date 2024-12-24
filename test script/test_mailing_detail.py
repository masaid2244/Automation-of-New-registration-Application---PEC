import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.LoginPage import LoginPage
from pages.MailingDetailsPage import MailingDetailsPage

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode
    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    yield driver
    driver.quit()

def test_login_and_fill_form(driver):
    login_page = LoginPage(driver)
    mailing_details_page = MailingDetailsPage(driver)

    login_page.open_login_page("http://10.0.32.90:8012/")
    login_page.login("pectesting12345@gmail.com", "pec123")

    mailing_details_page.click_wizstep2()

    mailing_details_page.select_value((By.ID, "select2-mailingdetails_country-container"), "Pakistan")
    mailing_details_page.select_value((By.ID, "select2-mailingdetails_province-container"), "Punjab")
    mailing_details_page.select_value((By.ID, "select2-mailingdetails_district-container"), "BAHAWALNAGAR")
    mailing_details_page.select_value((By.ID, "select2-mailingdetails_city-container"), "CHISHTIAN")

    mailing_details_page.enter_address("abcdefg absdg ghs shs ")
    mailing_details_page.submit_form()

    mailing_details_page.handle_alert()
    mailing_details_page.handle_modal()

    # Assert that the success message is displayed
    mailing_details_page.verify_success_message()
