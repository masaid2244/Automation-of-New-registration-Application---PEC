import pytest
from pages.interview_page import InterviewPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_interview_page(driver):
    interview_page = InterviewPage(driver)

    # Open the login page and perform login
    interview_page.open_login_page("http://10.0.32.90:8012/")
    interview_page.login("pectesting12345@gmail.com", "pec123")

    # Click on 'wizstep3a' and perform the subsequent steps
    interview_page.click_wizstep3a()

    # Upload files
    interview_page.upload_file("upload_file", r"F:\1pec\test data\Test  data pec\1.5mb.pdf")
    interview_page.upload_file("expupload_file", r"F:\1pec\test data\Test  data pec\1.5mb.pdf")

    # Submit interview details
    interview_page.click_submit()

    # Handle the modal dialog and assert the header
    interview_page.handle_modal_dialog()
    interview_page.assert_modal_header("Uploading of Documents")
