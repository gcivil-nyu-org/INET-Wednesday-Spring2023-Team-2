from django.test import TestCase
from posts.forms import CommentsForm, PollForm


class TestCommentFormValid(TestCase):
    def test_comment_form(self):
        comment_data = {"comment_text": "This is a test comment"}
        form = CommentsForm(data=comment_data)
        self.assertTrue(form.is_valid())


class TestPollFormValid(TestCase):
    def test_poll_form_valid(self):
        form_data = {
            "prefix": "Show of hands if",
            "question": "Testing questions",
            "delay": "8",
            "category": "entertainment",
            "choice1": "Yes",
            "choice2": "No",
            "choice3": "",
            "choice4": "",
        }
        form = PollForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_poll_form_invalid_no_prefix(self):
        form_data = {
            "prefix": "",
            "question": "Testing questions",
            "delay": "0",
            "category": "entertainment",
            "choice1": "Yes",
            "choice2": "No",
            "choice3": "",
            "choice4": "",
        }
        form = PollForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_poll_form_invalid_no_required(self):
        form_data = {
            "prefix": "Show of hands if",
            "question": "",
            "delay": "8",
            "category": "entertainment",
            "choice1": "Yes",
            "choice2": "",
            "choice3": "",
            "choice4": "",
        }
        form = PollForm(data=form_data)
        self.assertFalse(form.is_valid())
