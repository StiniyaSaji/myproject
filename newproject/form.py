from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from newproject.models import UploadImage


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = '__all__'

