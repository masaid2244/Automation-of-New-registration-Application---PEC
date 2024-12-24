import time

from selenium.common.exceptions import TimeoutException, \
    WebDriverException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def safe_click(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            print(f"Error interacting with element: {e}")
            self.capture_screenshot(f"error_{locator[1]}")
            raise

    def enter_text(self, locator, text):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            ).send_keys(text)
            print(f"Entered text '{text}' into element with locator {locator}.")
        except Exception as e:
            print(f"Error entering text into element with locator {locator}: {e}")
            self.capture_screenshot(f"text_error_{locator[1]}.png")

    def retry_click(self, locator, attempts=3):
        for i in range(attempts):
            try:
                self.scroll_and_click(locator)
                break
            except Exception as e:
                print(f"Retry {i + 1}/{attempts} failed: {e}")
                time.sleep(1)

    def wait_for_overlay_to_disappear(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sweet-overlay"))
            )
            print("Overlay has disappeared.")
        except TimeoutException:
            print("Timeout: Overlay did not disappear within the given time.")
            self.capture_screenshot("overlay_timeout_error.png")

    def clear_and_set_value(self, element, value):
        try:
            element.clear()
            time.sleep(1)  # Small delay to ensure the field is cleared
            element.send_keys(value)
            print(f"Successfully set value '{value}' in element {element.get_attribute('id')}.")
        except Exception as e:
            print(f"Error setting value '{value}' in element {element.get_attribute('id')}: {e}")
            self.capture_screenshot(f"set_value_error_{element.get_attribute('id')}.png")

    def wait_for_overlay_to_disappear(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sweet-overlay"))
            )
            print("Overlay has disappeared.")
        except TimeoutException:
            print("Timeout: Overlay did not disappear within the given time.")
            self.capture_screenshot("overlay_timeout_error.png")
    def scroll_and_click(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
            print(f"Successfully clicked element with locator {locator}.")
            self.capture_screenshot(f"clicked_{locator[1]}.png")
        except ElementClickInterceptedException:
            print(f"Element click intercepted for locator {locator}.")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))
            print(f"Successfully clicked element with locator {locator} using JavaScript.")
            self.capture_screenshot(f"clicked_{locator[1]}_js.png")
        except Exception as e:
            print(f"Error clicking element with locator {locator}: {e}")
            self.capture_screenshot(f"click_error_{locator[1]}.png")
    def capture_screenshot(self, filename):
        try:
            self.driver.get_screenshot_as_file(filename)
            print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

    def click_element(self, locator, wait_time=10):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            print(f"Error clicking element with locator {locator}: {e}")
            self.capture_screenshot(f"click_error_{locator[1]}.png")


def scroll_and_click(self, locator):
    try:
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        # Scroll to the element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Wait until element is clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()
        print(f"Clicked on element with locator: {locator}")
    except Exception as e:
        print(f"Error scrolling and clicking element with locator {locator}: {e}")
        self.capture_screenshot("scroll_and_click_error.png")

    def retry_click(self, locator, attempts=3):
        for i in range(attempts):
            try:
                self.scroll_and_click(locator)
                break
            except Exception as e:
                print(f"Retry {i + 1}/{attempts} failed: {e}")
                time.sleep(1)

    def remove_file(driver, xpath):
        try:
            remove_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            remove_button.click()
            print(f"Successfully clicked remove button for XPath: {xpath}")
            time.sleep(2)  # Wait for the removal to complete
        except Exception as e:
            print(f"Error removing existing file for XPath {xpath}: {e}")

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
        
    def select_first_value(self, element_id, value):
        try:
            dropdown = Select(WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            ))
            dropdown.select_by_visible_text(value)
        except WebDriverException:
            dropdown_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            dropdown_element.click()
            option_to_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
            )
            option_to_select.click()
