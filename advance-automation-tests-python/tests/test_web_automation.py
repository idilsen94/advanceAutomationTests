import unittest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Browser configuration settings
BROWSER_CONFIG = {
    'chrome': [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080"
    ],
    'firefox': [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080"
    ]
}

def setup_logging():
    """Initializes and configures  the logging system"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger

class WebTestFramework(unittest.TestCase):
    """Base framework for web automation testing with multi-browser support"""
    SUPPORTED_BROWSERS = ['chrome', 'firefox']
    active_browser = 'chrome'  # Default browser selection

    def initialize_webdriver(self):
        """Creates and configures WebDriver for the selected browser"""
        try:
            if self.active_browser == 'chrome':
                options = ChromeOptions()
                for config in BROWSER_CONFIG['chrome']:
                    options.add_argument(config)
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)

            elif self.active_browser == 'firefox':
                options = FirefoxOptions()
                for config in BROWSER_CONFIG['firefox']:
                    options.add_argument(config)
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            else:
                raise ValueError(f"Browser type '{self.active_browser}' is not supported")

            driver.implicitly_wait(5)
            driver.maximize_window()
            print(f"Successfully initialized {self.active_browser.capitalize()} WebDriver")
            return driver

        except Exception as e:
            print(f"Failed to initialize {self.active_browser}: {e}")
            raise

    def setUp(self):
        """Sets up test environment before each test"""
        self.driver = self.initialize_webdriver()
        self.logger = setup_logging()
        self.logger.info(f"Starting test execution with {self.active_browser.upper()} browser")
        self.test_start_time = datetime.utcnow()

    def tearDown(self):
        """Cleans up test environment after each test"""
        test_name = self._testMethodName
        if self.driver:
            if hasattr(self, '_outcome'):
                result = self._outcome.result
                if len(result.failures) > 0 or len(result.errors) > 0:
                    self._capture_failure_screenshot(test_name)
            self.driver.quit()

    def _capture_failure_screenshot(self, test_name):
        """Takes a screenshot when a test fails"""
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        screenshot_path = f"screenshots/{test_name}_{self.active_browser}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

    @classmethod
    def execute_all_browsers(cls):
        """Runs test suite across all supported browsers"""
        test_results = []
        for browser in cls.SUPPORTED_BROWSERS:
            print(f"\n{'=' * 50}")
            print(f"Executing tests with {browser.upper()} browser")
            print(f"{'=' * 50}")
            cls.active_browser = browser
            test_suite = unittest.TestLoader().loadTestsFromTestCase(cls)
            result = unittest.TextTestRunner().run(test_suite)
            test_results.append(result.wasSuccessful())

        return all(test_results)

    def get_driver(self):
        """Returns the current WebDriver instance"""
        return self.driver

    def get_logger(self):
        """Returns the current logger instance"""
        return self.logger

if __name__ == '__main__':
    unittest.main() 