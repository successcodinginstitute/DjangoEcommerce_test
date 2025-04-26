from django import forms
from django.contrib.auth.models import User
from django import forms

# Example of RequestDemoForm
class RequestDemoForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# Example of SalesInquiryForm
class SalesInquiryForm(forms.Form):
    company_name = forms.CharField(max_length=100)
    contact_email = forms.EmailField()
    inquiry_details = forms.CharField(widget=forms.Textarea)

# Example of CustomerSupportForm
class CustomerSupportForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    support_issue = forms.CharField(widget=forms.Textarea)
    contact_email = forms.EmailField()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data




from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'contact_number', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }