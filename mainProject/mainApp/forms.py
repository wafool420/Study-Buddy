# mainApp/forms.py
from django import forms
from .models import Profile, Post, Comment, Reply

class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    
    class Meta:
        model = Profile
        fields = ['pf_picture', 'bio', 'course_tag']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # when editing, pre-fill username from the related User
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
    
    def save(self, commit=True):
        profile = super().save(commit=False)

        # update the related User's username
        new_username = self.cleaned_data.get('username')
        user = profile.user
        if new_username:
            user.username = new_username

        if commit:
            user.save()
            profile.save()

        return profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']  # user will be set in the view

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        image = cleaned_data.get('image')

        # don't allow completely empty posts
        if not text and not image:
            raise forms.ValidationError("Post must have text or an image.")

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        

