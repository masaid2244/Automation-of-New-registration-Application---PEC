from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DomicileDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wizstep3_button = (By.ID, "wizstep3")
        self.country_dropdown = (By.ID, "select2-domiciledetails_country-container")
        self.province_dropdown = (By.ID, "select2-domiciledetails_province-container")
        self.district_dropdown = (By.ID, "select2-domiciledetails_district-container")
        self.address_field = (By.ID, "domiciledetails_address")
        self.remove_button = (By.XPATH, '//*[@id="dropzoneDomicile"]/div[2]/a[1]')
        self.upload_element = (By.ID, "dropzoneDomicile")
        self.submit_button = (By.ID, "btnSubmitDomicileDetails")
        self.modal_button1 = (By.XPATH, "/html/body/div[6]/div[7]/button[2]")
        self.modal_button2 = (By.XPATH, "//*[@id='domicile-modal']/div/div/div[3]/button[3]")
        self.header_modal = (By.XPATH, '//*[@id="Interview-modal"]/div/div/div[1]/h4')

    def select_value(self, dropdown_locator, value):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(dropdown_locator)).click()
        option_locator = (By.XPATH, f"//li[text()='{value}']")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option_locator)).click()

    def enter_address(self, address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.address_field)).send_keys(address)

    def click_wizstep3(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.wizstep3_button)).click()
            print("Successfully clicked wizstep3.")
        except Exception as e:
            print(f"Error clicking wizstep3: {e}")

    def remove_existing_file(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remove_button)).click()
            print("Existing file removed.")
            time.sleep(2)  # Wait for removal to complete
        except Exception as e:
            print(f"Error removing existing file: {e}")

    def upload_file(self, file_path):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.upload_element)).send_keys(file_path)
            print("New file uploaded.")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def submit_form(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit_button)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.modal_button1)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.modal_button2)).click()

    def verify_modal_header(self, expected_text):
        try:
            header_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.header_modal)
            )
            actual_text = header_element.text
            assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
            print("Assertion passed: Header text is correct.")
        except Exception as e:
            print(f"Error during assertion or modal handling: {e}")
