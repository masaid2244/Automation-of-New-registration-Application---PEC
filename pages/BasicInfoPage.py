from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.base_page import BasePage


class BasicInfoPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.gender_dropdown = "select2-basicinfo_gender-container"
        self.application_type_dropdown = "select2-ApplicationType-container"
        self.blood_group_dropdown = "select2-basicinfo_bloodGroup-container"
        self.submit_button = (By.ID, "btnSubmitBasicInfo")
        self.ok_button = (By.XPATH, "//button[text()='OK']")
        self.next_button = (By.XPATH, "//button[contains(@class, 'btn-info') and text()='Next']")
        self.assertion_element = (By.XPATH, "//h4[text()='Mailing Details']")

    def select_gender(self, gender):
        self.select_first_value(self.gender_dropdown, gender)

    def select_application_type(self, application_type):
        self.select_first_value(self.application_type_dropdown, application_type)

    def select_blood_group(self, blood_group):
        self.select_first_value(self.blood_group_dropdown, blood_group)

    def submit_basic_info(self):
        self.click_element(self.submit_button)
        self.click_element(self.ok_button)
        self.click_element(self.next_button)

    def assert_basic_info_page(self):
        try:
            # Wait until the element is visible, or time out after 10 seconds
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.assertion_element)
            )
            element_basic_assertion = self.driver.find_element(*self.assertion_element)
            if element_basic_assertion.is_displayed():
                print("Basic info page pass")
            else:
                print("Basic info page fail - Element is not visible")
        except NoSuchElementException:
            print("Basic info page fail - Element not found")
        except TimeoutException:
            print("Basic info page fail - Element not visible in time")
