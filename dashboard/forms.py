from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Group, Vehicle, Ride
from django.core.exceptions import ValidationError
from  .backend import DateTimePicker

# validation functions
def validate_positive(value):
    if value <= 0:
        raise ValidationError("Should be positive!")

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
                'placeholder':"%d/%m/%Y %H:%M",
            }
        )
    )
    class Meta:
        model = Profile
        fields = ['mobile', 'dob', 'gender']


class RideRequestForm(forms.ModelForm):
    dest = forms.CharField(
        label="Destination",
        widget=forms.Textarea(
            attrs={'cols': '10', 'rows': '1',
                   'placeholder': 'Enter your address here.'}),
        min_length=0,
        max_length=100,
    )

    arrive_time = forms.DateTimeField(
        label="Desired Arrival Time",
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': "dd/mm/yyyy hh:mm",
            }
        )
    )
    passengerNum = forms.IntegerField(
        label= "Passenger Number",
        widget=forms.NumberInput(
            attrs={'cols': '5', 'rows': '1',
                   'placeholder': 'Enter number here.'}),
        max_value=10, min_value=1
    )

    class Meta:
        model = Ride
        fields = ['dest', 'arrive_time', 'passengerNum',
                  'vehicleType', 'if_share']

    # def clean(self, *args, **kwargs):
    #     cleaned_data = self.cleaned_data
    #     vehicleType = cleaned_data.get('vehicleType')
    #     numPassengers = cleaned_data.get("numPassengers")
    #     vtinfo = VehicleTypeInfo()
    #     if numPassengers <= 0:
    #         raise forms.ValidationError(
    #             "The passenger num should be positive."
    #         )
    #     if (vtinfo.max_capacity[vehicleType] <= numPassengers):
    #         raise forms.ValidationError(
    #             "The passenger num is greater than the capacity of %s."
    #             % (vtinfo.type_choices[vehicleType][1])
    #         )
    #     return cleaned_data
