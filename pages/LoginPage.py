from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "btn-login")
        self.sign_in_link = (By.LINK_TEXT, "Sign In")

    def open_login_page(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def login(self, username, password):
        self.safe_click(self.sign_in_link)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.username_input)).send_keys(username)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
        self.safe_click(self.login_button)
