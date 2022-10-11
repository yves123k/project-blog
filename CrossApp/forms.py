from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import Textarea
from CrossApp.models import Comments, Create_Ad

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "password1", "password2", "is_active")
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     print(username)
    #     if len(username) < 3:
    #         raise forms.ValidationError("username too short")
    #     if " " in username:
    #         raise forms.ValidationError(" username must not contain space ")
    #     if not username.isalnum():
    #         raise forms.ValidationError("username must not contain number")
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=15)

class UpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "photo", "phoneNumber", "description", "address",
                  "website",'job',)

class AdForm(forms.ModelForm):
    class Meta:
        model = Create_Ad
        fields =( 
                'titre',
                'image',
                'price_on_sale',
                'price_for_rent',
                'living_area',
                'total_area',
                'nbres_pieces',
                'property_type',
                'year_built',
                'for_rent',
                'on_sale',
                'address',
                'more_info',)

class formAc(forms.Form):
    email = forms.EmailField(max_length=155)
    message = forms.Textarea()

class FormComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)

class FormContact(forms.Form):
    email = forms.EmailField(max_length=155)
    message = forms.CharField(widget=forms.Textarea)   