# reviewer/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Subject, Topic, Choice, Question

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["title", "description", "is_public"]

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "explanation"]     # adjust field names

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "explanation"]


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=("text", "is_correct"),
    extra=4,          # show 4 blank choices
    can_delete=False, # no delete checkboxes for now
    # no min_num/validate_min to avoid weird validation until everything works
)
