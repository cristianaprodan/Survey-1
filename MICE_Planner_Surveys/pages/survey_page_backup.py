from MICE_Planner_Surveys.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SurveyPage(BasePage):
    url = ""
    base_url = "https://analytics.staging.trustyou.com/surveys/site/reviews/ty?survey_id="

    def __init__(self, survey_id, driver):
        super(SurveyPage, self).__init__(driver)

        self.url = self.base_url + survey_id + "&lang=en"
        self.navigate()

    def find_question_by_id(self,question_id):
        question=self.driver.find_element_by_css_selector(".question[id*=" + self.fix_ids_starts_with_digit(question_id) + "]")
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

    def check_question_is_mandatory(self, id):
        mandatory_question = self.find_question_by_id(id).find_elements_by_css_selector('.mandatory_field')
        return mandatory_question

    def get_question_type(self, id):
        question= self.driver.find_element_by_id(id)
        question_type=question.find_element_by_class_name('field').get_attribute('data-type')
        return question_type

    def set_answer_for_rating(self, value_answer):
        overall_question = self.wait_until_element_is_visible((By.ID, 'overallrating'))
        overall_question.find_element_by_css_selector('li[data-value="' + str(value_answer) + '"]').click()
    def set_answer_for_describe_your_experience(self, review_text):
        review_question = self.driver.find_element_by_id('text')
        self.wait_until_element_is_visible(review_question)
        review_question.send_keys(review_text)

    def set_answer_for_rating_custom_question(self, question_id, value_answer):
        locator = (By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id)))
        question_rating = self.driver.find_element(locator[0], locator[1])
        self.wait_until_element_is_visible(locator)
        question_rating.find_element_by_css_selector('li[data-value="{}"]'.format(value_answer)).click()


    def set_anwser_for_radio_custom_question(self, question_id ,value_for_answer):
        locator = (By.CSS_SELECTOR, ".question[id*='{}']".format(self.fix_ids_starts_with_digit(question_id)))
        radio_question = self.driver.find_element(locator[0],locator[1])
        self.wait_until_element_is_visible(locator)
        radio_question.find_element_by_css_selector("input[value='" + str(value_for_answer) + "']").click()

    def set_answer_for_dropdowns_custom_question(self, fixed_id, value_for_answer):
        locator = (By.ID, self.fix_ids_starts_with_digit(fixed_id))
        dropdowns_question = self.driver.find_element(locator[0], locator[1])
        self.wait_until_element_is_visible(locator)
        dropdowns_question.find_element_by_css_selector ('option[value="' + str(value_for_answer) + '"]').click()

    def set_answer_for_text_custom_question(self, fixed_id, answer_text):
        locator = (By.ID, fixed_id)
        text_question = self.driver.find_element_by_id(locator)
        self.wait_until_element_is_visible(locator)
        text_question.send_keys(answer_text)

    def set_answer_for_data_question(self, fixed_id):
        data_question = self.driver.find_element_by_id(fixed_id)
        # data_question.find_element_by_css_

    def click_next(self):
        locator = (By.ID, 'next-button')
        next_button = self.driver.find_element_by_class_name(locator)
        self.wait_until_element_is_visible(locator)
        next_button.click()

    def enter_email(self,email_text):
        locator = (By.ID, 'quest_email')
        email_field = self.driver.find_element_by_id(locator)
        self.wait_until_element_is_visible(locator)
        email_field.send_keys(email_text)


    def get_submit_button(self):
        locator = (By.ID, 'submit-button')
        submit_button = self.driver.find_element_by_id(locator)
        self.wait_until_element_is_visible(locator)
        return submit_button