from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from pages.base_page import BasePage

class DegreeDetailPage(BasePage):  # Inherit from BasePage
    def __init__(self, driver):
        super().__init__(driver)  # Initialize BasePage
        self.driver = driver

    def handle_modal_alert(self):
        try:
            modal_ok_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
            )
            modal_ok_button.click()
            print("Successfully clicked the OK button on the modal alert.")
            self.capture_screenshot("modal_alert_ok_clicked.png")
            time.sleep(2)  # Wait for the alert to disappear
        except TimeoutException:
            print("No modal alert found to handle.")
        except Exception as e:
            print(f"Error handling modal alert: {e}")
            self.capture_screenshot("modal_alert_error.png")

    def safe_upload_file(self, dropzone_id, file_path):
        try:
            dropzone_form = (By.ID, dropzone_id)
            dropzone_message = (By.CLASS_NAME, "dz-message")

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(dropzone_form)
            )
            dropzone = self.driver.find_element(*dropzone_form)
            dropzone.click()
            self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)

            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(dropzone_message)
            )
            print(f"File uploaded successfully to {dropzone_id}.")
            self.capture_screenshot(f"upload_success_{dropzone_id}.png")
        except Exception as e:
            print(f"Exception occurred while uploading the file to {dropzone_id}: {e}")
            self.capture_screenshot(f"upload_exception_{dropzone_id}.png")
            self.handle_modal_alert()  # Handle modal alert if present
            try:
                dropzone = self.driver.find_element(*dropzone_form)
                dropzone.click()
                self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)
            except Exception as retry_exception:
                print(f"Retry failed for file upload to {dropzone_id}: {retry_exception}")
                self.capture_screenshot(f"retry_upload_exception_{dropzone_id}.png")

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

    def click_save_button(self, locator):
        try:
            self.wait_for_overlay_to_disappear()
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(locator)
            ).click()
            print("Save action successful.")
            time.sleep(2)

            success_message_locator = (By.CSS_SELECTOR, ".success-message")
            success_message = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(success_message_locator)
            )
            assert success_message.is_displayed(), "Success message not displayed, save action might have failed."
            print("Assertion passed: Success message displayed.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Save button click was intercepted.")
            self.capture_screenshot("save_button_intercepted.png")
        except Exception as e:
            print(f"Error clicking save button: {e}")
            self.capture_screenshot("save_button_error.png")

    def fill_degree_details(self):
        # Ensure 'wizstep6' is clicked before proceeding
        self.scroll_and_click((By.ID, "wizstep6"))

        # Clear and set values in form fields
        grad_institute_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "grad_institute"))
        )
        self.clear_and_set_value(grad_institute_element, "UET Lahore")

        grad_program_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "grad_program"))
        )
        self.clear_and_set_value(grad_program_element, "Bsc")

        grad_passingyear_field = self.driver.find_element(By.ID, "grad_passingyearForeign")
        self.clear_and_set_value(grad_passingyear_field, "10-Aug-2005")

        grad_percentage_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "grad_percentage"))
        )
        self.clear_and_set_value(grad_percentage_element, "87.12")

        # Remove files from different dropzones
        xpaths = [
            '//*[@id="dropzoneEngDMC"]/div[2]/a[1]',
            '//*[@id="dropzoneEngCertificate"]/div[2]/a[1]',
        ]
        for xpath in xpaths:
            self.remove_file(xpath)

        # Upload files
        self.safe_upload_file("dropzoneEngDMC", r"F:\1pec\test data\Test data pec\download (1).jpg")
        self.safe_upload_file("dropzoneEngCertificate", r"F:\1pec\test data\Test data pec\download (1).jpg")

        # Click the save button once and assert success
        self.click_save_button((By.ID, "btnSubmitGradDetails"))
