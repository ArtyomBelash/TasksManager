from django import forms
from django.contrib.auth.models import User

from .models import Tasks, Profile


class TaskCreateAndUpdateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'style': 'resize:none',})
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
