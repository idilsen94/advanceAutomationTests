import time

from selenium.webdriver.common.by import By

from pages.base_page import WebPageBase


class QualityAssurancePortal(WebPageBase):
    """Handles QA careers portal interactions and job search"""
    # Page element locators
    BTN_VIEW_ALL_JOBS = (By.LINK_TEXT, 'See all QA jobs')
    DROPDOWN_LOCATION = (By.ID, 'select2-filter-by-location-container')
    OPTION_ISTANBUL = (By.CSS_SELECTOR, '.select2-results__option:nth-of-type(2)')
    DROPDOWN_DEPARTMENT = (By.ID, 'select2-filter-by-department-container')
    JOB_LIST_HEADER = (By.CLASS_NAME, 'currentResult')
    JOB_TITLE = (By.CSS_SELECTOR, '.position-title')
    JOB_DEPARTMENT = (By.CSS_SELECTOR, '.position-department')
    JOB_LOCATION = (By.CSS_SELECTOR, '.position-location')
    JOB_LIST = (By.CSS_SELECTOR, '.position-list-item')
    BTN_VIEW_ROLE = (By.LINK_TEXT, 'View Role')

    # Page URLs and expected values
    PORTAL_URL = 'https://useinsider.com/careers/quality-assurance/'
    APPLICATION_URL = 'lever'
    REQUIRED_POSITION = "Quality Assurance"
    REQUIRED_DEPARTMENT = "Quality Assurance"
    REQUIRED_LOCATION = "Istanbul, Turkey"

    def open_job_listings(self):
        """Opens the complete list of QA job positions"""
        self.perform_click(*self.BTN_VIEW_ALL_JOBS)

    def open_location_filter(self):
        """Opens the location filter dropdown"""
        self.perform_click(*self.DROPDOWN_LOCATION)

    def select_location(self, *location_element):
        """Selects a location from the filter dropdown"""
        self.perform_click(*location_element)

    def get_position_title(self):
        """Gets the job position title"""
        return self.extract_text(self.JOB_TITLE)

    def get_position_department(self):
        """Gets the job position department"""
        return self.extract_text(self.JOB_DEPARTMENT)

    def get_position_location(self):
        """Gets the job position location"""
        return self.extract_text(self.JOB_LOCATION)

    def initiate_application(self):
        """Starts the job application process"""
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        time.sleep(1)
        self.perform_hover(*self.JOB_TITLE)
        time.sleep(1)
        self.perform_click(*self.BTN_VIEW_ROLE)

    def switch_to_application_window(self):
        """Switches to the application form window"""
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

    def validate_job_listings(self):
        """Validates all job listings against required criteria"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        time.sleep(2)
        job_items = self.driver.find_elements(*self.JOB_LIST)
        
        for job in job_items:
            title = job.find_element(*self.JOB_TITLE).text
            department = job.find_element(*self.JOB_DEPARTMENT).text
            location = job.find_element(*self.JOB_LOCATION).text.replace('Turkiye', 'Turkey')

            if not (
                    (self.REQUIRED_POSITION in title or "QA" in title) and
                    self.REQUIRED_DEPARTMENT in department and
                    self.REQUIRED_LOCATION in location
            ):
                print(f"""
                Job listing validation failed:
                Expected Position: {self.REQUIRED_POSITION}, Found: {title}
                Expected Department: {self.REQUIRED_DEPARTMENT}, Found: {department}
                Expected Location: {self.REQUIRED_LOCATION}, Found: {location}
                """)
                return False
        return True

    def get_selected_department(self):
        """Gets the currently selected department"""
        return self.extract_clean_text(self.DROPDOWN_DEPARTMENT)
