import time

import selenium
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

class DropzonePage:
    def __init__(self, driver):
        self.driver = driver

    def upload_file(self, dropzone_id, file_path):
        dropzone_form = (By.ID, dropzone_id)
        dropzone_message = (By.CLASS_NAME, "dz-message")

        try:
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
            capture_screenshot(f"upload_success_{dropzone_id}.png")
        except TimeoutException:
            print(f"Error: File upload to {dropzone_id} failed due to timeout.")
            capture_screenshot(f"upload_error_{dropzone_id}.png")
        except Exception as e:
            print(f"Error: File upload to {dropzone_id} failed. Exception: {e}")
            capture_screenshot(f"upload_error_{dropzone_id}.png")


def select_value_by_text(element_id, value):
    try:
        for _ in range(3):  # Retry mechanism
            try:
                # Wait for the dropdown element to be clickable
                dropdown_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, element_id))
                )
                dropdown_element.click()

                # Wait until the dropdown options are fully loaded
                option_xpath = f"//li[contains(text(), '{value}')]"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )

                # Find and click the option that matches the text
                option_to_select = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option_to_select.click()
                return  # Exit after successful selection

            except StaleElementReferenceException:
                print(f"StaleElementReferenceException encountered. Retrying... ({value})")
                time.sleep(1)  # Wait before retrying
                continue

        print(f"Error selecting value '{value}' for '{element_id}': Element not interactable after retries.")
        capture_screenshot(f"dropdown_error_{element_id}")

    except WebDriverException as e:
        print(f"Error selecting value '{value}' for '{element_id}': {e}")
        capture_screenshot(f"dropdown_error_{element_id}")


def remove_file(xpath):
    try:
        remove_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        remove_button.click()
        print(f"Successfully clicked remove button for XPath: {xpath}")
        time.sleep(2)  # Wait for the removal to complete
    except Exception as e:
        print(f"Error removing existing file for XPath {xpath}: {e}")
        capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")


def capture_screenshot(filename):
    try:
        if not filename.endswith(".png"):
            filename += ".png"
        driver.get_screenshot_as_file(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

# Function to scroll to the element and click it
def scroll_and_click(locator):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()
        print(f"Successfully clicked element with locator {locator}.")
        capture_screenshot(f"clicked_{locator[1]}.png")
    except ElementClickInterceptedException:
        print(f"Element click intercepted for locator {locator}. Trying JavaScript click.")
        driver.execute_script("arguments[0].click();", driver.find_element(*locator))
        print(f"Successfully clicked element with locator {locator} using JavaScript.")
        capture_screenshot(f"clicked_{locator[1]}_js.png")
    except Exception as e:
        print(f"Error clicking element with locator {locator}: {e}")
        capture_screenshot(f"click_error_{locator[1]}.png")


# Navigate to the website and perform actions
driver.get("http://10.0.32.90:8012/")
driver.maximize_window()

# Perform login
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))
).click()

element_username = driver.find_element(By.ID, "username")
element_username.send_keys("abdullahqureshi914@gmail.com")

element_password = driver.find_element(By.ID, "password")
element_password.send_keys("pecreg81202039")

element_signin_button = driver.find_element(By.ID, "btn-login")
element_signin_button.click()

# Scroll and click on the desired menu item
scroll_and_click((By.XPATH, "//*[@id='mainnav-menu']/li[7]/a"))
driver.implicitly_wait(10)

# Example usage: Select values from the dropdown
select_value_by_text("select2-renewalBranchOffice-container", "PEC HQ ISLAMABAD")
select_value_by_text("select2-ddlMailingProvince-container", "AJK")
select_value_by_text("select2-ddlMailingDistrict-container", "BHIMBER")
select_value_by_text("select2-ddlMCity-container", "BHIMBER")
select_value_by_text("select2-ddlMailingCountry-container", "Pakistan")

# Fill the address field
address_element = driver.find_element(By.ID, "renewalPostalAddress")
address_element.clear()
address_element.send_keys("Abc test 123")

# Remove existing files
xpaths = [
    '//*[@id="dropzoneProfilePic"]/div[2]/a[1]',
    '//*[@id="dropzoneCnicBackPic"]/div[2]/a[1]',
    '//*[@id="dropzoneCnicPic"]/div[2]/a[1]',
    '//*[@id="dropzoneSignaturePic"]/div[2]/a[1]'
]

for xpath in xpaths:
    remove_file(xpath)

# Upload new files
dropzone_page = DropzonePage(driver)
dropzone_page.upload_file("dropzoneProfilePic", r"F:\1pec\test data\Test  data pec\erd1.png")  # Profile
dropzone_page.upload_file("dropzoneSignaturePic", r"F:\1pec\test data\Test  data pec\erd1.png")  # Signature
dropzone_page.upload_file("dropzoneCnicPic", r"F:\1pec\test data\Test  data pec\erd1.png")  # CNIC
dropzone_page.upload_file("dropzoneCnicBackPic", r"F:\1pec\test data\Test  data pec\erd1.png")  # CNIC Back

# Submit the form
driver.find_element(By.ID, "btnAddressSubmit").click()
driver.implicitly_wait(15)
driver.find_element(By.XPATH, "/html/body/div[5]/div[7]/button[2]").click()
print(f"test case 1 pass ")
driver.find_element(By.XPATH, "//*[@id='demo-bv-tab1']/div[2]/button").click()
driver.implicitly_wait(5)
driver.find_element(By.XPATH, "//*[@id='demo-bv-tab2']/div[4]/div[2]/button").click()
driver.implicitly_wait(5)
driver.find_element(By.ID, "btn-employment").click()

select_value_by_text("select2-ddlEmpType-container", "Employed (Public Sector)")
select_value_by_text("select2-ddlExpertise-container", "Advanced Methods of Structural Analysis")

#driver.find_element(By.ID, "txtToDate").send_keys("10-aug-2023")
driver.implicitly_wait(3)
driver.find_element(By.ID, "txtEmployerName").send_keys("PEC")
driver.implicitly_wait(2)
driver.find_element(By.ID, "txtDesignation").send_keys("TEST")
#driver.find_element(By.ID, "txtFromDate").send_keys("10-jan-2024")
driver.implicitly_wait(3)
driver.find_element(By.ID, "txtExpertise").send_keys("PEC 123 123 123 ")

# Remove any existing file in the employment dropzone if necessary
#remove_file("//*[@id='dropzoneEmployment']/div[2]/a[1]")
date_element = driver.find_element(By.ID, "txtFromDate")

# Clear any pre-filled value
date_element.send_keys(Keys.BACKSPACE * 10)  # Optional: Clear existing value

# Step 1: Enter the partial date '20-June-'
date_element.send_keys("20-June ")

# Step 2: Press the left arrow key 4 times to move the cursor to the left (to before the year section)
date_element.send_keys(Keys.ARROW_LEFT * 4)

# Step 3: Enter the year '2021'
date_element.send_keys("2021")

try:
    date_element.send_keys("20-June ")
    print("Partial date '20-June ' entered successfully.")
except Exception as e:
    print(f"Error entering partial date: {e}")
    capture_screenshot("date_partial_error.png")

# Step 2: Press the left arrow key 4 times to move the cursor to the left (to before the year section) and debug
try:
    date_element.send_keys(Keys.ARROW_LEFT * 4)
    print("Left arrow key pressed 4 times successfully.")
except Exception as e:
    print(f"Error pressing left arrow key: {e}")
    capture_screenshot("arrow_key_error.png")

# Step 3: Enter the year '2021' and debug the input
try:
    date_element.send_keys("2021")
    print("Year '2021' entered successfully.")
except Exception as e:
    print(f"Error entering year '2021': {e}")
    capture_screenshot("year_entry_error.png")

# Verify the date value in the input field
try:
    entered_date = date_element.get_attribute("value")
    print(f"Date entered in the field: {entered_date}")
    if entered_date != "20-June-2021":
        print("Warning: The entered date does not match the expected value '20-June-2021'.")
except Exception as e:
    print(f"Error retrieving the entered date value: {e}")
    capture_screenshot("date_value_error.png")

# Optional: Pause to ensure the date is set
time.sleep(1)
# Locate the txtToDate element
to_date_element = driver.find_element(By.ID, "txtToDate")

# Clear any pre-filled value
to_date_element.send_keys(Keys.BACKSPACE * 10)  # Optional: Clear existing value

# Step 1: Enter the partial date '20-Aug-'
to_date_element.send_keys("20-Aug ")

# Step 2: Press the left arrow key 4 times to move the cursor to the left (to before the year section)
to_date_element.send_keys(Keys.ARROW_LEFT * 4)

# Step 3: Enter the year '2024'
to_date_element.send_keys("2024")

# Debugging steps for each part
try:
    to_date_element.send_keys("20-Aug ")
    print("Partial date '20-Aug ' entered successfully.")
except Exception as e:
    print(f"Error entering partial date for txtToDate: {e}")
    capture_screenshot("to_date_partial_error.png")

try:
    to_date_element.send_keys(Keys.ARROW_LEFT * 4)
    print("Left arrow key pressed 4 times successfully for txtToDate.")
except Exception as e:
    print(f"Error pressing left arrow key for txtToDate: {e}")
    capture_screenshot("to_date_arrow_key_error.png")

try:
    to_date_element.send_keys("2024")
    print("Year '2024' entered successfully for txtToDate.")
except Exception as e:
    print(f"Error entering year '2024' for txtToDate: {e}")
    capture_screenshot("to_date_year_entry_error.png")

# Verify the date value in the txtToDate input field
try:
    entered_to_date = to_date_element.get_attribute("value")
    print(f"Date entered in the txtToDate field: {entered_to_date}")
    if entered_to_date != "20-Aug-2024":
        print("Warning: The entered date does not match the expected value '20-Aug-2024'.")
except Exception as e:
    print(f"Error retrieving the entered date value for txtToDate: {e}")
    capture_screenshot("to_date_value_error.png")

# Optional: Pause to ensure the date is set
time.sleep(1)

# Upload file after date input for txtToDate
try:
    dropzone_page.upload_file("dropzoneEmployment", r"F:\1pec\test data\Test  data pec\erd1.png")
    print("File uploaded successfully after txtToDate entry.")
except Exception as e:
    print(f"Error uploading file after txtToDate entry: {e}")
    capture_screenshot("file_upload_after_to_date_error.png")

# Upload file after date input
try:
    dropzone_page.upload_file("dropzoneEmployment", r"F:\1pec\test data\Test  data pec\erd1.png")
    print("File uploaded successfully after date entry.")
except Exception as e:
    print(f"Error uploading file after date entry: {e}")
    capture_screenshot("file_upload_after_date_error.png")

#driver.find_element(By.XPATH,"/html/body/div[6]/div[7]/button[2]")

# Pause to ensure the date is set (optional)
time.sleep(1)

dropzone_page.upload_file("dropzoneEmployment", r"F:\1pec\test data\Test  data pec\erd1.png")
driver.implicitly_wait(15)
driver.find_element(By.ID , "btnSubmitEmployment").click()
driver.implicitly_wait(15)

try:
    # Wait and click on the first button to ensure it is clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[7]/button[2]"))
    ).click()
    print("First button clicked successfully")

    # Wait and click on the second button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='demo-bv-tab3']/div[3]/div[2]/button"))
    ).click()
    print("Second button clicked successfully")

    print("TEST CASE NO 2 PASS")

    # Wait and click on the third button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='demo-bv-tab4']/div[4]/div[2]/button"))
    ).click()
    print("Third button clicked successfully")

except selenium.common.exceptions.ElementNotInteractableException as e:
    print(f"ElementNotInteractableException occurred: {str(e)}")
    # You can add additional logging or screenshots here for debugging

except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
driver.find_element(By.ID,"chkboxDeclaration").click()

try:
    # Wait for the interview modal to appear
    header_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="btnSubmitApp"]'))
    )

    # Assert that the header text matches the expected value
    expected_text = "Submit Renewal Application"  # Replace with actual expected text
    actual_text = header_element.text
    assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
    print("Assertion passed: Header text is correct.")
except Exception as e:
    print(f"Error during assertion or modal handling: {e}")
    capture_screenshot("assertion_error")
