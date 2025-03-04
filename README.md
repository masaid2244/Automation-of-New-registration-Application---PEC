# Engineer Registration Portal Automation 
# New Application (Engineer Registration) PEC

This project automates the engineer registration process on PEC portal using **Python** and **Selenium**. The goal of this project is to simplify and accelerate the process of registering a new engineer by automating repetitive steps involved in the registration of application submission.

## Key Features:
- **Automated Engineer Registration**: Automates the process of entering details for new engineer applications through the portal.
- **Selenium WebDriver**: Uses Selenium WebDriver for browser automation, simulating user interactions with the registration portal.
- **Page Object Model (POM)**: Implements the Page Object Model (POM) design pattern for better organization and maintainability of the code. Each page on the portal is represented by a separate Python class, making the code modular and easier to scale.
- **Cross-browser Testing**: The automation is built to be compatible with multiple browsers (e.g., Chrome, Firefox), ensuring flexibility in testing.

## Technologies Used:
- **Python**: The programming language used for automation scripting.
- **Selenium**: The web automation tool used to interact with the registration portal.
- **Page Object Model (POM)**: A design pattern used to structure the code for easy maintenance and scalability.
- **WebDriver**: Selenium's WebDriver for simulating browser interactions.

## Project Structure:
- **Page Objects**: Each page on the portal has its own corresponding Python class under the `pages` directory, following the POM pattern.
- **Tests**: The `tests` directory contains test scripts that execute the registration automation process.

## Setup & Installation:
1. Clone the repository: `git clone <repository_url>`
2. Install the required Python dependencies: `pip install -r requirements.txt`
3. Configure WebDriver (ChromeDriver, GeckoDriver, etc.) as per the browser you're using.
4. Run the tests: `python -m unittest discover`

