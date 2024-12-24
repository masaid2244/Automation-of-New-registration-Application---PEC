from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class UndergradDetailsPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wizstep5_button = (By.ID, "wizstep5")
        self.dropdown_ids = {
            "matric_board": "select2-matric_board-container",
            "matric_certificate": "select2-matric_program-container",
            "matric_batchyear": "select2-matric_batchyear-container",
            "matric_passyear": "select2-matric_passingyear-container",
            "inter_board": "select2-inter_board-container",
            "inter_certificate": "select2-inter_program-container",
            "inter_batch": "select2-inter_batchyear-container",
            "inter_passyear": "select2-inter_passingyear-container",
        }
        self.percentages = {
            "matric_percentage": (By.ID, "matric_percentage"),
            "inter_percentage": (By.ID, "inter_percentage"),
        }
        super().__init__(driver)

    def click_wizstep5(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.wizstep5_button)).click()
            print("Successfully clicked wizstep5.")
        except Exception as e:
            print(f"Error clicking wizstep5: {e}")
            self.capture_screenshot("click_wizstep5_error.png")

    def select_dropdown_value(self, dropdown_id, value):
        try:
            dropdown_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            dropdown_element.click()

            # Wait for the dropdown options to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//li[text()='{value}']"))
            )

            option_to_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
            )
            option_to_select.click()
            print(f"Selected {value} from dropdown {dropdown_id}.")
        except Exception as e:
            print(f"Error selecting value {value} for dropdown {dropdown_id}: {e}")
            self.capture_screenshot(f"dropdown_error_{dropdown_id}.png")

    def enter_percentage(self, field_id, value):
        try:
            percentage_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, field_id))
            )
            percentage_element.clear()
            percentage_element.send_keys(value)
            print(f"Entered {value} in percentage field {field_id}.")
        except Exception as e:
            print(f"Error entering percentage in field {field_id}: {e}")
            self.capture_screenshot(f"percentage_error_{field_id}.png")

    def remove_file(self, xpath):
        try:
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            remove_button.click()
            print(f"Successfully clicked remove button for XPath: {xpath}")
            time.sleep(2)  # Wait for the removal to complete
        except Exception as e:
            print(f"Error removing file for XPath {xpath}: {e}")
            self.capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")

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
        self.retry_click((By.ID, "btnSubmitUndergradDetails"))
        self.driver.implicitly_wait(4)

        # Handling modal dialog
        self.retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
        self.retry_click((By.XPATH, "//*[@id='undergrad-modal']/div/div/div[3]/button[4]"))

        # Perform assertion after clicking the modal button
        try:
            header_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="grad-modal"]/div/div/div[1]/h4'))
            )
            expected_text = "Qualification Details"  # Replace with actual expected text
            actual_text = header_element.text
            assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
            print("Assertion passed: Header text is correct.")
        except Exception as e:
            print(f"Error during assertion or modal handling: {e}")
            self.capture_screenshot("assertion_error.png")
