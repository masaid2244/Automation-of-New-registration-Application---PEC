import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.LoginPage import LoginPage
from pages.DomicileDetailsPage import DomicileDetailsPage

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
    domicile_details_page = DomicileDetailsPage(driver)

    login_page.open_login_page("http://10.0.32.90:8012/")
    login_page.login("pectesting12345@gmail.com", "pec123")

    # Correctly call click_wizstep3 on the instance of DomicileDetailsPage
    domicile_details_page.click_wizstep3()

    # Interact with the domicile details page
    domicile_details_page.select_value((By.ID, "select2-domiciledetails_country-container"), "Pakistan")
    domicile_details_page.select_value((By.ID, "select2-domiciledetails_province-container"), "Punjab")
    domicile_details_page.select_value((By.ID, "select2-domiciledetails_district-container"), "BAHAWALNAGAR")

    domicile_details_page.enter_address("abcd efg123")
    domicile_details_page.remove_existing_file()
    domicile_details_page.upload_file("F:/1pec/test data/SampleJPGImage_1mbmb.jpg")

    domicile_details_page.submit_form()

    # Assert the modal header text
    domicile_details_page.verify_modal_header("Assessment/Interview Details")
