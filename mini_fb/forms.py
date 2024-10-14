from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 1920, -1)), required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url', 'birth_date']


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']