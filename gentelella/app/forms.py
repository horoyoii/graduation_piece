from django import forms

class DeviceForm(forms.Form):
    name = forms.CharField(max_length=30)
    you = forms.CharField(max_length=30)


