from django import forms
from .models import *
from django.contrib.auth.models import User

class BlogPostForm(forms.ModelForm):
    class Meta:
        model  = BlogPost
        fields = ("image", "title", 'category', 'body')

        widgets = {
            "image": forms.FileInput(attrs={
                "class": "file_upload-input",
                'onchange': 'readURL(this);'
            }),
            
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter the title of the blog...',
                "class": 'form-control'
                }),

            "category": forms.Select(attrs={
                "class": "form-control"
            }),

            'body': forms.TextInput(attrs={
                "class": 'form-control',
                "type": "hidden"
                })
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

        widgets = {
            "username": forms.TextInput(attrs = {
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs = {
                "class": "form-control",
            }),
            "password": forms.PasswordInput(attrs = {
                "class": "form-control",
            })
        }