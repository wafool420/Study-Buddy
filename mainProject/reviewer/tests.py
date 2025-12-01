from django.test import TestCase
from .models import Subject, Topic, Question, Choice

class QuestionTest(TestCase):
    def test_create_question_with_choices(self):
        s = Subject.objects.create(title="Math", slug="math")
        t = Topic.objects.create(subject=s, title="Algebra")
        q = Question.objects.create(topic=t, text="2+2?")
        Choice.objects.create(question=q, text="3", is_correct=False)
        Choice.objects.create(question=q, text="4", is_correct=True)
        self.assertEqual(q.choices.count(), 2)
