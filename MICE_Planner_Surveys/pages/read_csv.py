import csv


with open("/home/user/Downloads/OPER-6733 Accor Templates - MICE_Planner_questions.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    question_type = ''
    question_answer = 5
    count = 0

    representation_mapping = {
        (2, 6): "Rating",
        (1, 1): "Text",
        (3, 5): "Radio",
        (3, 4): "Dropdown",
        (5, 8): "Rating",
        (7, 1): "Date",
        (6, 9): "Message",
    }
    for row in reader:

        question_representation = int(row['question_type'])
        representation_type = int(row['representation_type'])

        question_type = representation_mapping[(question_representation, representation_type)]

        question_id = row['master_id']
        question_answer = 5
        if count == 10:
            print("self.page.click_next()")
            count = 0
        elif question_type == 'Message':
            print("self.page.submit_button")

        print(
            "self.page.set_answer_for_question('{0}', '{1}', {2})".format(question_id, question_type, question_answer))
        count += 1

