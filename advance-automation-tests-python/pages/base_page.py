from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class WebPageBase:
    """Base class for web page interactions"""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def perform_click(self, *locator):
        """Clicks on the specified element"""
        self.driver.find_element(*locator).click()

    def perform_hover(self, *locator):
        """Hovers over the specified element"""
        element = self.driver.find_element(*locator)
        hover_action = ActionChains(self.driver).move_to_element(element)
        hover_action.perform()

    def get_page_url(self):
        """Gets the current page URL"""
        return self.driver.current_url

    def wait_for_element(self, locator, timeout=20):
        """
        Wait for element to be clickable
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element

        """
        return self.wait.until(locator, ec.element_to_be_clickable, timeout)

    def extract_text(self, locator):
        """Gets text from the specified element"""
        return self.wait_for_element(locator).text

    def extract_clean_text(self, locator):
        """Gets cleaned text from the specified element"""
        text = self.wait_for_element(locator).text
        return text.replace('×\n', '').strip()

    def check_element_visibility(self, locator, message=''):
        """Checks if element is visible"""
        return self.wait.until(ec.visibility_of_element_located(locator), message)

    def navigate_to(self, url):
        """Navigates to the specified URL"""
        self.driver.get(url)
