from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Note Title', 
                'class': 'input-title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Start typing your notes here...', 
                'class': 'input-content'
            }),
        }