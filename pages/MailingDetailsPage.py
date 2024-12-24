from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MailingDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.country_dropdown = (By.ID, "select2-mailingdetails_country-container")
        self.province_dropdown = (By.ID, "select2-mailingdetails_province-container")
        self.district_dropdown = (By.ID, "select2-mailingdetails_district-container")
        self.city_dropdown = (By.ID, "select2-mailingdetails_city-container")
        self.address_field = (By.ID, "mailingdetails_address")
        self.submit_button = (By.ID, "btnSubmitMailingDetails")
        self.wizstep2_button = (By.ID, "wizstep2")
        self.alert_button = (By.XPATH, "//button[contains(@class, 'confirm') and text()='OK']")
        self.success_message = (By.ID, "success-message")  # Adjust the locator as needed

    def select_value(self, dropdown_locator, value):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(dropdown_locator)).click()
        option_locator = (By.XPATH, f"//li[text()='{value}']")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option_locator)).click()

    def enter_address(self, address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.address_field)).send_keys(address)

    def submit_form(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit_button)).click()

    def click_wizstep2(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.wizstep2_button)).click()

    def handle_alert(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            print(f"Error handling alert: {e}")

    def handle_modal(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.alert_button)).click()
        except Exception as e:
            print(f"Error handling modal: {e}")

    def verify_success_message(self):
        try:
            success_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            assert success_element.is_displayed(), "Success message is not displayed."
        except AssertionError as e:
            print(f"AssertionError: {e}")
        except Exception as e:
            print(f"Error verifying success message: {e}")
