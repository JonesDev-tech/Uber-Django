from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]

# Override clean() function in forms, to verify if the input is legal
class ProfileForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder':"YYYY-mm-dd",
            }
        )
    )
    class Meta:
        model = Profile
        fields = ['mobile', 'dob', 'gender']


# class UserCreationForm(forms.ModelForm):
#     """
#     A form that creates a user, with no privileges, from the given username and
#     password.
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     password1 = forms.CharField(label=_("Password"),
#         widget=forms.PasswordInput)
#     password2 = forms.CharField(label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#         help_text=_("Enter the same password as above, for verification."))
#
#     class Meta:
#         model = User
#         fields = ("username",)
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
