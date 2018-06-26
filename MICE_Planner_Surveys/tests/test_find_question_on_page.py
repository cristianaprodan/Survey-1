import unittest
from selenium import webdriver
import csv
from MICE_Planner_Surveys.pages.survey_page import SurveyPage


class TestQuestionId(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = SurveyPage("bc8e5b9b-f5c5-4005-b379-55cf73c6502d", self.driver)
        self.csvfile = open("/home/user/Downloads/OPER-6733 Accor Templates - MICE_Planner_questions.csv", 'r')


    def test_search_for_question(self):

        # parse CSV
        spamreader = csv.reader(self.csvfile, delimiter=',')
        # skip header
        next(spamreader, None)
        # for each row
        question_count = 0
        question_limit = 10
        for row in spamreader:
            #  get question id
            expected_question_id = row[1]
            # should the question appear ?
            if row[-2] == '' and question_count < question_limit:
                #   find  on page
                question_element = self.page.find_question_by_id(expected_question_id)

                self.assertTrue(question_element, 'Question ID %s was not found' % expected_question_id)
                print('Question ID %s was found' % expected_question_id)
                # increase questions count
                question_count += 1
                # answer question
                # does it trigger another question
                if self.question_should_be_mandatory(row):
                    question_mandatory = self.page.check_question_is_mandatory(expected_question_id)
                    self.assertTrue(question_mandatory, "Question %s is not mandatory as expected" % expected_question_id)
    ### helper functions ###

    def question_should_be_mandatory(self, question_row):
        mandatory_column = 8
        return question_row[mandatory_column] == 't'


    def check_if_answer_is_selected(self,id,):
        expected_status="is-selected.is active"
        status=self.driver.find_element_by_class_name()
        self.assertEqual(expected_status, status)

    def tearDown(self):
        self.driver.close()
        self.csvfile.close()

if __name__ == "__main__":
    unittest.main()
