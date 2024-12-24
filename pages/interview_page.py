from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from pages.LoginPage import LoginPage
from pages.base_page import BasePage

class InterviewPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.login_page = LoginPage(driver)

    def open_login_page(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.login_page.login(username, password)

    def click_wizstep3a(self):
        self.safe_click((By.ID, "wizstep3a"))

    def upload_file(self, input_id, file_path):
        absolute_path = os.path.abspath(file_path)
        if os.path.exists(absolute_path):
            print(f"Uploading file from path: {absolute_path}")
            try:
                self.driver.find_element(By.ID, input_id).send_keys(absolute_path)
                print(f"File uploaded successfully to {input_id}.")
            except Exception as e:
                print(f"Error uploading file: {e}")
                self.capture_screenshot(f"upload_error_{input_id}.png")
        else:
            print(f"File does not exist at path: {absolute_path}. Please check the file path.")

    def click_submit(self):
        self.retry_click((By.ID, "btnSubmitInterviewDetail"))

    def handle_modal_dialog(self):
        self.retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
        self.retry_click((By.XPATH, "//*[@id='Interview-modal']/div/div/div[3]/button[3]"))

    def assert_modal_header(self, expected_text):
        try:
            header_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="documents-modal"]/div/div/div[1]/h4'))
            )
            actual_text = header_element.text
            assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
            print("Assertion passed: Header text is correct.")
        except Exception as e:
            print(f"Error during assertion or modal handling: {e}")
            self.capture_screenshot("assertion_error.png")
