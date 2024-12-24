from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class DocumentDetailPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wizstep4_button = (By.ID, "wizstep4")
        super().__init__(driver)

    def remove_file(self, xpath):
        try:
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            remove_button.click()
            print(f"Successfully clicked remove button for XPath: {xpath}")
            time.sleep(2)  # Wait for the removal to complete
        except Exception as e:
            print(f"Error removing existing file for XPath {xpath}: {e}")
            self.capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")

    def click_wizstep4(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.wizstep4_button)).click()
            print("Successfully clicked wizstep4.")
        except Exception as e:
            print(f"Error clicking wizstep4: {e}")

    def upload_file(self, dropzone_id, file_path):
        dropzone_form = (By.ID, dropzone_id)
        dropzone_message = (By.CLASS_NAME, "dz-message")

        # Wait until the dropzone is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(dropzone_form)
        )

        # Click on the dropzone to open the file dialog
        dropzone = self.driver.find_element(*dropzone_form)
        dropzone.click()

        # Upload the file by sending the file path
        self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)

        # Optional: Wait for the upload to complete
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(dropzone_message)
        )
        print(f"File uploaded successfully to {dropzone_id}.")
        self.capture_screenshot(f"upload_success_{dropzone_id}.png")

    def handle_modals(self):
        # Click the submit button
        self.retry_click((By.ID, "btnSubmitDocumentDetails"))
        self.driver.implicitly_wait(4)

        # Handling modal dialog
        self.retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
        self.retry_click((By.XPATH, "//*[@id='documents-modal']/div/div/div[3]/button[3]"))

        # Perform assertion after clicking the modal button
        try:
            # Wait for the interview modal to appear
            header_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="undergrad-modal"]/div/div/div[1]/h4'))
            )

            # Assert that the header text matches the expected value
            expected_text = "Undergrad Details"  # Replace with actual expected text
            actual_text = header_element.text
            assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
            print("Assertion passed: Header text is correct.")
        except Exception as e:
            print(f"Error during assertion or modal handling: {e}")
            self.capture_screenshot("assertion_error")
