import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pages.DegreeDetailpage import DegreeDetailPage
from pages.base_page import BasePage
from pages.LoginPage import LoginPage
from pages.DegreeDetailpage import DegreeDetailPage

@pytest.fixture
def driver():
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("http://10.0.32.90:8012/")
    driver.maximize_window()
    login_page = LoginPage(driver)
    login_page.open_login_page("http://10.0.32.90:8012/")
    login_page.login("pectesting12345@gmail.com", "pec123")

    yield driver
    driver.quit()

def test_degree_details(driver):
    page = DegreeDetailPage(driver)

    # Handle any modal alerts that might appear
    page.handle_modal_alert()

    # Perform the actions related to degree details
    page.fill_degree_details()
