from django.contrib.auth.models import User

class CustomBackend(object):
    def authenticate(request, **credentials):
        username = credentials.get('username', credentials.get('username'))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return user

    def get_user(user_id):
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