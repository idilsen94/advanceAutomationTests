from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import WebPageBase


class MainPage(WebPageBase):
    """Handles main website and careers portal interactions"""
    # Main page element locators
    NAV_COMPANY = (By.XPATH, "//a[contains(text(), 'Company')]")
    NAV_CAREERS = (By.LINK_TEXT, 'Careers')
    
    # Careers portal element locators
    SECTION_LOCATIONS = (By.ID, 'career-our-location')
    SECTION_TEAMS = (By.LINK_TEXT, 'See all teams')
    SECTION_CULTURE = (By.XPATH, "//h2[contains(text(), 'Life at Insider')]")
    
    # Page URLs
    BASE_URL = 'https://useinsider.com/'

    def verify_page_load(self):
        """Verifies main page has loaded correctly"""
        self.wait.until(ec.visibility_of_element_located(self.NAV_COMPANY), 
                       'Company navigation element not found on page')

    def hover_company_menu(self):
        """Hovers over the Company navigation menu"""
        self.perform_hover(*self.NAV_COMPANY)

    def select_careers_option(self):
        """Clicks the Careers option in Company menu"""
        self.perform_click(*self.NAV_CAREERS)

    def verify_careers_sections(self):
        """Checks if all required careers sections are visible"""
        locations_visible = self.check_element_visibility(self.SECTION_LOCATIONS)
        teams_visible = self.check_element_visibility(self.SECTION_TEAMS)
        culture_visible = self.check_element_visibility(self.SECTION_CULTURE)
        
        return all([locations_visible, teams_visible, culture_visible])
