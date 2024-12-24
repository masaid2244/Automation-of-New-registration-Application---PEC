import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.Documentdetailpage import DocumentDetailPage
from pages.DomicileDetailsPage import DomicileDetailsPage
from pages.base_page import BasePage
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

def test_document_detail_page(setup):
    driver = setup

    # Perform login
    login_page = LoginPage(driver)
    login_page.open_login_page("http://10.0.32.90:8012/")
    login_page.login("pectesting12345@gmail.com", "pec123")

    # Ensure 'wizstep4' is clicked before proceeding
    document_page = DocumentDetailPage(driver)
    document_page.click_wizstep4()

    # Remove files from different dropzones
    xpaths = [
        '//*[@id="dropzoneProfile"]/div[2]/a[1]',
        '//*[@id="dropzoneSignature"]/div[2]/a[1]',
        '//*[@id="dropzoneCNIC"]/div[2]/a[1]',
        '//*[@id="dropzoneCNIC2"]/div[2]/a[1]'
    ]

    for xpath in xpaths:
        document_page.remove_file(xpath)

    # Upload files using the DocumentDetailPage class
    file_paths = {
        "dropzoneProfile": r"F:\1pec\test data\Test  data pec\1.jpeg",  # Profile
        "dropzoneCNIC2": r"F:\1pec\test data\Test  data pec\1.jpeg",  # CNIC2
        "dropzoneSignature": r"F:\1pec\test data\Test  data pec\1.jpeg",  # Signature
        "dropzoneCNIC": r"F:\1pec\test data\Test  data pec\1.jpeg"  # CNIC
    }

    for dropzone_id, file_path in file_paths.items():
     document_page.upload_file(dropzone_id, file_path)


    print(f"Waiting for file to be visible in {dropzone_id}")

    try:
        file_uploaded_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[@id='{dropzone_id}']/div[1]/div[1]/img"))
        )
        assert file_uploaded_element.is_displayed(), f"File upload failed for {dropzone_id}."
        print(f"File upload verified successfully for {dropzone_id}.")
    except Exception as e:
        print(f"Error verifying file upload for {dropzone_id}: {e}")
        document_page.capture_screenshot(f"upload_error_{dropzone_id}.png")
    # Handle modals
    document_page.handle_modals()

    # Verify that the modal handling was successful
    try:
        # Wait for the undergrad modal to appear and check its header text
        header_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="undergrad-modal"]/div/div/div[1]/h4'))
        )
        expected_text = "Undergrad Details"  # Replace with actual expected text
        actual_text = header_element.text
        assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
        print("Assertion passed: Header text is correct.")
    except Exception as e:
        print(f"Error during assertion or modal handling: {e}")
        document_page.capture_screenshot("assertion_error")
