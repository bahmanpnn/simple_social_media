from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ProfileUser


class RegisterForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'username'
    }))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'email',
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'confirm password'
    }))


    def clean_email(self):
        email=self.cleaned_data['email']
        if email=='':
            raise ValidationError('please fill email field too!!')
        
        user=User.objects.filter(email=email).exists()

        if user:
            raise ValidationError('this email used before!! please register again with another email :))')
        
        return email
    
    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()

        if user:
            raise ValidationError('this username exists and used before!! please use another username')
        
        return username
    

    def clean(self):
        cd=super().clean()

        password=cd.get('password')
        confirm_password=cd.get('confirm_password')

        if password and confirm_password and password !=confirm_password:
            raise ValidationError('password with confirm password does not match!! check again please')


class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'username'
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'password'
    }))

class ProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control bg-light',
    }))

    class Meta:
        model=ProfileUser
        fields=('age','phone_number','bio')

        widgets={
            'age':forms.TextInput(attrs={
                'class':'form-control bg-light',
            }),
            'phone_number':forms.TextInput(attrs={
                'class':'form-control bg-light',
            }),
            'bio':forms.Textarea(attrs={
                'class':'form-control bg-light',
                'rows':2,
            })
        }