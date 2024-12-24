from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time

class ChallanPage:
    def __init__(self, driver):
        self.driver = driver

    def scroll_and_click(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)
            print(f"Successfully clicked element with locator {locator}.")
        except TimeoutException:
            print(f"Timeout while trying to click element with locator {locator}.")

    def select_bank(self, bank_name):
        try:
            bank_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "bank-dropdown"))
            )
            bank_dropdown.click()
            bank_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//option[text()='{bank_name}']"))
            )
            bank_option.click()
            print(f"Selected bank: {bank_name}.")
        except TimeoutException:
            print(f"Timeout while trying to select bank {bank_name}.")

    def fill_challan_details(self, doc_no, date, amount):
        try:
            doc_no_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "doc_no"))
            )
            date_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "date"))
            )
            amount_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "amount"))
            )
            doc_no_field.send_keys(doc_no)
            date_field.send_keys(date)
            amount_field.send_keys(amount)
            print("Challan details filled successfully.")
        except TimeoutException:
            print("Timeout while trying to fill challan details.")

    def remove_file(self, xpath):
        try:
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", remove_button)
            print(f"Successfully clicked remove button with XPath {xpath}.")
        except TimeoutException:
            print(f"Timeout while trying to click remove button with XPath {xpath}.")

    def upload_file(self, input_id, file_path):
        try:
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, input_id))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
            file_input.send_keys(file_path)
            print(f"File {file_path} uploaded successfully.")
        except TimeoutException:
            print(f"Timeout while trying to upload file {file_path}.")
        except ElementNotInteractableException:
            print(f"ElementNotInteractableException: The file input element was not interactable.")

    def ensure_element_interactable(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except Exception as e:
            print(f"Error ensuring element interactable for locator {locator}: {e}")
            self.capture_screenshot(f"element_interactable_error_{locator[1]}.png")
            return None

    def submit_challan(self):
        self.click_save_button((By.ID, "btnSubmitChallanDetails"))

    def click_save_button(self, locator):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sweet-overlay"))
            )
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            save_button.click()
            print("Clicked save button.")
            time.sleep(2)

            # Check if the file was uploaded by verifying the presence of the uploaded file element
            file_uploaded_locator = (By.XPATH, "//div[contains(text(), '1.5mb.pdf')]")  # Adjust locator as needed
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(file_uploaded_locator)
            )
            print("File upload verification successful.")
        except TimeoutException:
            print("TimeoutException: Could not find the success message after clicking save button.")
