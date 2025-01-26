from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import random


class LoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('username','password')

    usernameattrs = {
    'placeholder':'Enter your Username',
    'name':'username',
    'class':'form-control',
    'id':'username',
    }
    passwordattrs = {
    'placeholder':'Enter your Password',
    'name':'password',
    'class': 'form-control',
    'id':'pwd',
    }
    username = forms.CharField(max_length=255,min_length=6,required=True,label='Username:',
                               widget=forms.TextInput(attrs=usernameattrs))
    password = forms.CharField(max_length=255,min_length=8,required=True,label='Password:',
                               widget=forms.PasswordInput(attrs=passwordattrs))

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ('username','password','password_confirm')
    
    
         
        
    
       
    usernameattrs = {
    'placeholder':'Enter your Username',
    'name':'username',
    'class':'form-control',
    'id':'username',
    }
    passwordattrs = {
    'placeholder':'Enter your Password',
    'name':'password',
    'class': 'form-control',
    'id':'password',
    }
    confpasswordattrs = {
        'placeholder':'Enter your Password Again',
        'name':'password-confirm',
        'class': 'form-control',
        'id':'password',
    }
    username = forms.CharField(max_length=255,min_length=6,required=True,label='Username: ',
                               widget=forms.TextInput(attrs=usernameattrs))
    password = forms.CharField(max_length=255,min_length=8,required=True,label='Password: ',
                               widget=forms.PasswordInput(attrs=passwordattrs))
    password_confirm = forms.CharField(max_length=255,min_length=8,required=True,label='Passowrd Confirm',
                                       widget=forms.PasswordInput(attrs=confpasswordattrs))
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        # user.set_color(random.choice(self.colors))
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and (password != password_confirm):
            raise ValidationError("Passwords Do not match")
        return cleaned_data

    
