from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'username'
    }))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'email',
        'required':False
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'password'
    }))


    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        
        if user:
            raise ValidationError('this email used before!! please register again with another email :))')
        
        return email
    