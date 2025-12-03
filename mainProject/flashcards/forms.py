from django import forms
from .models import FlashcardSet, Flashcard


class FlashcardSetForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ["title", "description", "is_public"]


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ["term", "definition", "image"]
