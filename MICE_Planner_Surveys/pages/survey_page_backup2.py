from MICE_Planner_Surveys.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SurveyPage(BasePage):
    url = ""
    base_url = "https://analytics.staging.trustyou.com/surveys/site/reviews/ty?survey_id="

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

    def set_answer_for_rating(self, value_answer):
        overall_question = self.wait_until_element_is_visible((By.ID, 'overallrating'))
        overall_question.find_element_by_css_selector('li[data-value="' + str(value_answer) + '"]').click()

    def set_answer_for_describe_your_experience(self,text_review):
        review_question = self.wait_until_element_is_visible((By.ID, 'text'))
        review_question.send_keys(text_review)

    def set_answer_for_rating_custom_question(self, question_id, value_answer):
        question_rating = self.wait_until_element_is_visible((By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id))))
        question_rating.find_element_by_css_selector('li[data-value="{}"]'.format(value_answer)).click()

    def set_anwser_for_radio_custom_question(self, question_id, value_for_answer):
        radio_question = self.wait_until_element_is_visible((By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id))))
        radio_question.find_element_by_css_selector("input[value='" + str(value_for_answer) + "']").click()

    def set_answer_for_dropdowns_custom_question(self, question_id, value_for_answer):
        dropdowns_question = self.wait_until_element_is_visible((By.ID, self.fix_ids_starts_with_digit(question_id)))
        dropdowns_question.find_element_by_css_selector('option[value="' + str(value_for_answer) + '"]').click()

    def set_answer_for_text_custom_question(self, question_id, answer_text):
        text_question = self.wait_until_element_is_visible((By.ID, self.fix_ids_starts_with_digit(question_id)))
        text_question.send_keys(answer_text)

    def set_answer_for_data_question(self, fixed_id):
        data_question = self.driver.find_element_by_id(fixed_id)
        # data_question.find_element_by_css_

    def click_next(self):
        next_button = self.wait_until_element_is_visible((By.CLASS_NAME, 'next_button'))
        next_button.click()

    def enter_email(self,email_text):
        email_field = self.wait_until_element_is_visible((By.ID, 'guest_email'))
        email_field.send_keys(email_text)

    def get_submit_button(self):
        submit_button = self.wait_until_element_is_visible((By.ID, 'submit_button'))
        return submit_button

    def set_answer_for_question(self, question_id, question_type, question_answer):
        if question_type == 'RATING':
            self.set_answer_for_rating_custom_question(question_id, question_answer)