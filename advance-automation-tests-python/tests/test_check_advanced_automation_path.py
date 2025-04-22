import time

from pages.home_page import MainPage
from pages.qa_career_page import QualityAssurancePortal
from tests.test_web_automation import WebTestFramework


class CareerPortalAutomation(WebTestFramework):
    """
    Test suite for validating the career portal automation workflow:
    1. Verify main website accessibility and navigation
    2. Validate careers portal sections and content
    3. Test QA job search functionality with location and department filters
    4. Verify job listing criteria and details
    5. Validate application form redirection
    """

    def test_career_portal_workflow(self):
        """Executes the complete career portal automation workflow"""
        self.logger.info("Step 1: Verifying main website accessibility")
        main_page = MainPage(self.driver)
        main_page.navigate_to(main_page.BASE_URL)
        self.assertEqual(main_page.BASE_URL, main_page.get_page_url(),
                         'Main website URL verification failed')
        self.logger.info("Main website verification completed successfully")

        self.logger.info("Step 2: Validating careers portal sections")
        main_page.hover_company_menu()
        main_page.select_careers_option()

        self.assertTrue(main_page.verify_careers_sections(),
                        "One or more required sections not found on careers page")
        self.logger.info("Careers portal sections verified successfully")

        self.logger.info("Step 3: Executing QA job search with filters")
        qa_portal = QualityAssurancePortal(self.driver)
        main_page.navigate_to(qa_portal.PORTAL_URL)
        self.assertIn(qa_portal.PORTAL_URL, main_page.get_page_url(),
                      'QA portal URL verification failed')

        qa_portal.open_job_listings()
        qa_portal.verify_elements_loaded()
        qa_portal.open_location_filter()
        qa_portal.select_location(*qa_portal.OPTION_ISTANBUL)

        self.assertEqual(qa_portal.get_selected_department(), "Quality Assurance",
                         'QA department filter verification failed')
        self.assertTrue(qa_portal.check_element_visibility(qa_portal.JOB_LIST_HEADER),
                        "Job listings not displayed")
        self.logger.info("QA job search and filtering completed successfully")

        self.logger.info("Step 4: Validating job listing criteria")
        time.sleep(1)
        self.assertTrue(qa_portal.validate_job_listings(),
                        "Job listing criteria validation failed")
        self.logger.info("Job listing validation completed successfully")

        self.logger.info("Step 5: Verifying application form redirection")
        qa_portal.initiate_application()
        time.sleep(1)
        qa_portal.switch_to_application_window()
        self.assertIn(qa_portal.APPLICATION_URL, qa_portal.get_page_url(),
                      "Application form redirection failed")
        self.logger.info("Application form verification completed successfully")

    def tearDown(self):
        self.quit_driver()
