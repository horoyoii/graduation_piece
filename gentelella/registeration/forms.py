from django import forms

from .models import *


class ProfileFormModel(forms.ModelForm):
    class Meta:
        model = Device_profile
        fields = ['device_profile_file']