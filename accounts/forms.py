from django import forms
from .models import User
from .models import UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ["first_name", "last_name", "username", "email", "password"]

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get("password")
    confirm_assword = cleaned_data.get("confirm_password")

    if password != confirm_assword:
      raise forms.ValidationError("Password does not match")
    
class UserProfileForm(forms.ModelForm):
  address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "start typing...", "required": "required"}))
  profile_picture = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator])
  cover_photo = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator])

  latitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
  longitude = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
  class Meta:
    model = UserProfile
    fields = ["profile_picture", "cover_photo", "address", "country", "state", "city", "pin_code", "latitude", "longitude"]


# This is a function to replace longitude and latitude
# def __init__(self, *args, **kwargs):
#   super(UserProfile, self).__init__(*args, **kwargs)
#   for field in self.fields:
#     if field == "latitude" or field == "longitude":
#       self.fields[field].widget.attrs["readonly"] = "readonly"


class UserInfoForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "phone_number"]