class AnswersMixin:
    def __init__(self, items):
        self.items = items

    def check_in_text_select(self, item):
        correct = 0
        questions = 0
        answers = item.answer.data.get("answers")
        user_answers = item.answer.data.get("user")

        if user_answers is None:
            return None, None, False

        for key, val in answers.items():
            questions += 1
            if val == user_answers[key]:
                correct += 1
        return correct, questions, True

    def check_answer_choice(self, item):
        return int(item.answer.is_correct), True

    def check(self):
        correct = 0  # correct answers
        question_len = 0

        for item in self.items:
            if item.exercise.type == "IN_TEXT_SELECT":
                correct_in_text, questions, status = self.check_in_text_select(
                    item=item
                )
                if not status:
                    continue
                correct += correct_in_text
                question_len += questions

            elif item.exercise.type == "ANSWER_CHOICE":
                correct_answer_choice, status = self.check_answer_choice(item=item)
                if not status:
                    continue
                correct += correct_answer_choice
                question_len += 1
        return correct, question_len
