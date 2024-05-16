from django import forms

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