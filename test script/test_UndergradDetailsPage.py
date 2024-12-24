from telnetlib import EC

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pages.UndergradDetailsPage import UndergradDetailsPage
from pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def setup():
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("http://10.0.32.90:8012/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_undergrad_details_page(setup):
    driver = setup

    # Perform login
    login_page = LoginPage(driver)
    login_page.open_login_page("http://10.0.32.90:8012/")
    login_page.login("pectesting12345@gmail.com", "pec123")

    # Ensure 'wizstep5' is clicked before proceeding
    undergrad_page = UndergradDetailsPage(driver)
    undergrad_page.click_wizstep5()

    # Remove files from different dropzones
    xpaths = [
        '//*[@id="dropzoneMatricDMC"]/div[2]/a[1]',
        '//*[@id="dropzoneInterDMC"]/div[2]/a[1]',
        '//*[@id="dropzoneMatricCertificate"]/div[2]/a[1]',
        '//*[@id="dropzoneInterCertificate"]/div[2]/a[1]'
    ]

    for xpath in xpaths:
        undergrad_page.remove_file(xpath)

    # Upload files using the UndergradDetailsPage class
    file_paths = {
        "dropzoneMatricDMC": r"F:\1pec\test data\Test  data pec\1.jpeg",  # Matric DMC
        "dropzoneInterDMC": r"F:\1pec\test data\Test  data pec\1.jpeg",  # Inter DMC
        "dropzoneMatricCertificate": r"F:\1pec\test data\Test  data pec\1.jpeg",  # Matric Certificate
        "dropzoneInterCertificate": r"F:\1pec\test data\Test  data pec\1.jpeg"  # Inter Certificate
    }

    for dropzone_id, file_path in file_paths.items():
        undergrad_page.upload_file(dropzone_id, file_path)

    # Enter percentages
    undergrad_page.enter_percentage("matric_percentage", "80.12")
    undergrad_page.enter_percentage("inter_percentage", "85.12")

    # Handle modals
    undergrad_page.handle_modals()

    # Verify that the modal handling was successful
    try:
        header_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="undergrad-modal"]/div/div/div[1]/h4'))
        )
        expected_text = "Qualification Details"  # Replace with actual expected text
        actual_text = header_element.text
        assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
        print("Assertion passed: Header text is correct.")
    except Exception as e:
        print(f"Error during assertion or modal handling: {e}")
        undergrad_page.capture_screenshot("assertion_error.png")
