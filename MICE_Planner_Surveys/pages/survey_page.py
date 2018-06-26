import csv
import datetime
import time
import random

from MICE_Planner_Surveys.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SurveyPage(BasePage):
    url = ""
    base_url = "https://analytics.staging.trustyou.com/surveys/site/reviews/ty?survey_id="
    count = 0

    def __init__(self, survey_id, driver):
        super(SurveyPage, self).__init__(driver)

        self.url = self.base_url + survey_id + "&lang=en"
        self.navigate()

    def find_question_by_id(self, question_id):
        question = self.driver.find_element_by_css_selector(
            ".question[id*=" + self.fix_ids_starts_with_digit(question_id) + "]")
        return question

    def fix_ids_starts_with_digit(self, id):
        '''
        https://benfrain.com/when-and-where-you-can-use-numbers-in-id-and-class-names/
        according to Css standard,
        :param id:
        :return:
        '''
        # if the id don't starts with digit, the id will remain the same
        fixed_id = id
        # if id starts with digit
        if id[0].isdigit():
            # replace first digit with \\3 + digit + ' '
            fixed_id = ("\\3" + id[0] + " " + id[1:])
            # return the fixed id
        return fixed_id

    # test 1 : 2bf533fe-045f-49a3-a758-fd6defeb140e becomes \\32 bf533fe-045f-49a3-a758-fd6defeb140e
    # test 2 : d3430d3b-23c7-4ca7-b038-57f1682a0055 becomes d3430d3b-23c7-4ca7-b038-57f1682a0055

    def set_answer_for_rating(self, question_id='overallrating', value_answer='5'):
        # question type
        # the color for each answer
        # the text fot each answer
        # which scale is used(5 or 10)
        overall_question = self.wait_until_element_is_visible((By.ID, question_id))
        overall_question.find_element_by_css_selector('li[data-value="' + str(value_answer) + '"]').click()
        # self.count += 1

    def set_answer_for_describe_your_experience(self, question_id='text', text_review='Was good'):
        # the number of characters
        review_question = self.wait_until_element_is_visible((By.ID, question_id))
        review_question.send_keys(text_review)
        # self.count += 1

    def set_answer_for_rating_custom_question(self, question_id, value_answer):
        # question type
        # the color for each answer
        # the text fot each answer
        # which scale is used(5 or 10)
        question_rating = self.wait_until_element_is_visible(
            (By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id))))
        question_rating.find_element_by_css_selector('li[data-value="{}"]'.format(value_answer)).click()

    def set_anwser_for_radio_custom_question(self, question_id, value_for_answer):
        # how many answers are available
        radio_question = self.wait_until_element_is_visible(
            (By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id))))
        radio_question.find_element_by_css_selector("input[value='" + str(value_for_answer) + "']").click()

    def set_answer_for_dropdowns_custom_question(self, question_id, value_for_answer):
        dropdowns_question = self.wait_until_element_is_visible((By.ID, self.fix_ids_starts_with_digit(question_id)))
        dropdowns_question.find_element_by_css_selector('option[value="' + str(value_for_answer) + '"]').click()

    def set_answer_for_text_custom_question(self, question_id, answer_text):
        # how many answers are available
        text_question = self.wait_until_element_is_visible((By.ID, self.fix_ids_starts_with_digit(question_id)))
        text_question.send_keys(answer_text)

    def set_answer_for_date_question(self, question_id, date):
        text_question = self.wait_until_element_is_visible((By.ID, self.fix_ids_starts_with_digit(question_id)))
        text_question.send_keys(date)

    def check_message(self, question_id, dummy=None):
        message = self.wait_until_element_is_visible((By.CSS_SELECTOR,".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id))))
        return message

    def click_next(self):
        next_button = self.wait_until_element_is_visible((By.CLASS_NAME, 'next_button'))
        next_button.click()

    def enter_email(self, question_id, email_text):
        email_field = self.wait_until_element_is_visible((By.ID, question_id))
        email_field.send_keys(email_text)

    def get_submit_button(self):
        submit_button = self.wait_until_element_is_visible((By.ID, 'submit_button'))
        return submit_button

    def set_answer_for_question(self, question_id, question_type, question_answer):
        question_function_mapping = {
            "Rating": self.set_answer_for_rating_custom_question,
            "Text": self.set_answer_for_text_custom_question,
            "Radio": self.set_anwser_for_radio_custom_question,
            "Dropdown": self.set_answer_for_dropdowns_custom_question,
            "Date": self.set_answer_for_date_question,
            "Message": self.check_message,
            "overall_rating": self.set_answer_for_rating,
            "your_review": self.set_answer_for_describe_your_experience,
            "email_address": self.enter_email
        }

        question_function_mapping[question_type](question_id, question_answer)
        self.count += 1

    def get_calendar_date(self, days_adjusted):
        return (datetime.datetime.now() + datetime.timedelta(days=days_adjusted)).strftime('%Y-%m-%d')

    def select_answer_from_dependence(self, dependence_list):

        num_to_select = 1
        dependence_list = random.sample(dependence_list, num_to_select)
        answer= dependence_list[1]
        print(answer)


    def test_questions_from_csv_file(self, csvfile):
        with open(csvfile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            representation_mapping = {
                (2, 6): ("Rating", 5),
                (1, 1): ("Text", 'lorem'),
                (3, 5): ("Radio", 0),
                (3, 4): ("Dropdown", 1),
                (5, 8): ("Rating", 5),
                (7, 1): ("Date", self.get_calendar_date(0)),
                (6, 9): ("Message", ''),
                (9, 9): ("email", 'fake@mailinator.com'),
            }
            basic_questions = {'overall_rating': 'overallrating', 'your_review': 'text', 'email_address': 'guest_email'}
            for row in reader:

                question_representation = int(row['question_type'])
                representation_type = int(row['representation_type'])
                parent_question = int(row['parent_question'])
                dependece_list = int(row['dependence'])
                question_type = representation_mapping[(question_representation, representation_type)][0]
                question_answer = representation_mapping[(question_representation, representation_type)][1]

                question_id = row['master_id']

                for csv_question_type, html_question_id in basic_questions.items():
                    if question_id == csv_question_type:
                        question_id = html_question_id
                        question_type = csv_question_type
                        break

                if self.count == 10:
                    self.save_screenshot('/tmp/screenshot_{}.png'.format(time.time()))
                    self.click_next()
                    self.count = 0

                try:
                    if question_type == "email_address":
                        pass
                    self.set_answer_for_question(question_id, question_type, question_answer)
                except Exception as e:
                    print(repr(e) + " " + question_id)

            self.get_submit_button()
        # if question_type == 'Rating':
        #     self.set_answer_for_rating_custom_question(question_id, question_answer)
        # elif question_type== 'Text':
        #     self.set_answer_for_text_custom_question(question_id, question_answer)
        # elif question_type == 'Radio':
        #     self.set_anwser_for_radio_custom_question(question_id, question_answer)
        # elif question_type == 'Dropdown':
        #     self.set_answer_for_dropdowns_custom_question(question_id, question_answer)
        # elif question_type == 'Date':
        #     self.set_answer_for_date_question(question_id, question_answer)
