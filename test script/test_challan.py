from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.LoginPage import LoginPage
from pages.challan import ChallanPage
import time
from pages.base_page import BasePage
def test_challan_form():
    # Setup Chrome WebDriver
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Open the application
        driver.get("http://10.0.32.90:8012/")
        driver.maximize_window()

        # Login
        login_page = LoginPage(driver)
        login_page.login("pectesting12345@gmail.com", "pec123")

        # Navigate to Challan Page and fill details
        challan_page = ChallanPage(driver)
        challan_page.scroll_and_click((By.ID, "wizstep7"))
        challan_page.scroll_and_click((By.XPATH, "//*[@id='challan-modal']/div/div/div[2]/div[3]/div[2]/span"))

        # Select bank and fill in challan details
        challan_page.select_bank("Alfalah")
        challan_page.fill_challan_details("01589886", "10-Aug-2024", "5500")

        # Remove files
        xpaths = [
            '//*[@id="dropzoneChallan"]/div[2]/a[1]',
            # Add other XPaths if needed
        ]
        for xpath in xpaths:
            challan_page.remove_file(xpath)

        # Upload a new file
        # Add a delay to ensure the file input is ready (if necessary)
        time.sleep(2)
        challan_page.upload_file("dropzoneChallan", r"F:\1pec\test data\Test data pec\download (1).jpg")

        # Submit the form
        challan_page.submit_challan()

    finally:
        # Ensure the browser is closed
        driver.quit()

if __name__ == "__main__":
    test_challan_form()
