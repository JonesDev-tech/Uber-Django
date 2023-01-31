from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.forms import DateTimeInput

class CustomBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class VehicleInfo:
    capacity = [4, 5, 2, 4, 7]
    type = [(0, 'Sedan'),  #4
            (1, 'SUV'),  #4
            (2, 'Coupe'),  #2
            (3, 'Hatchback'),  #4
            (4, 'Mini van'),  #7
            ]
    description = "-Sedan: 4 door trunks, capacity: 4 <br/>\
        -SUV: Sport-Utility Vehicle, capacity: 5 <br/>\
        -Coupe: 2 door trunks, capacity: 2 <br/>\
        -Hatchback: Compact sedan, capacity: 4 <br/>\
        -Minivan: Trunks with large cargo area, capacity: 7 <br/>\
        * The capacity includes driver. "

class DateTimePicker(DateTimeInput):
    template_name = 'dashboard/DateTimePicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context