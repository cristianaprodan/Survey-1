import unittest
from selenium import webdriver
from MICE_Planner_Surveys.pages.survey_page import SurveyPage


class TestQuestionId(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = SurveyPage("bc8e5b9b-f5c5-4005-b379-55cf73c6502d", self.driver)
        self.csvfile = "/home/user/Downloads/OPER-6733 Accor Templates - MICE_Planner_questions.csv"

    def test_basic_question(self):
        # self.page.set_answer_for_rating()
        # self.page.set_answer_for_describe_your_experience('Was good')
        self.page.test_questions_from_csv_file(self.csvfile)
        # self.page.enter_email('palace@trustyou.com')
        self.assertTrue(self.page.get_submit_button().is_displayed(), 'Submit button is not visible')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
