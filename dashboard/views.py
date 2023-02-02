from django.shortcuts import get_object_or_404, redirect, render, render
from .forms import RegisterForm, ProfileForm, RideRequestForm, SearchRide
from .models import User, Profile, Ride, Group
# from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.views import generic
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
#TODO: Success 页面, edit删除ride所有共享成员, 邮件提醒
#TODO: 检查非法输入
# take second element for sort

def require_ride(request):
    if not request.session.get('is_login', None):
        return redirect('/login')

    if request.method == "POST":
        form = RideRequestForm(request.POST)
        curr_user = get_object_or_404(User, id=request.session['user_id'])
        if form.is_valid():
            ride = form.save(commit=False)
            ride.owner = curr_user
            try:
                group = Group.objects.get(user=curr_user, groupNum=ride.passengerNum)
            except Group.DoesNotExist:
                group = Group(user=curr_user, groupNum=ride.passengerNum)
                group.save()
            ride.save()
            ride.shared_by_user.add(group)
            messages.success(request, 'Request successfully.')
            return redirect("/")
        else:
            print("form not valid:"+str(form.errors))
    else:
        form = RideRequestForm()

    context = {'form': form}
    return render(request, 'dashboard/require_ride.html', context)

def started_ride(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    else:
        curr_user = get_object_or_404(User, id = request.session['user_id'])
        open_ride = Ride.objects.filter(
            confirmed=False,
            completed=False,
            owner = curr_user
        ).order_by("arrive_time")
        confirmed_ride = Ride.objects.filter(
            confirmed=True,
            completed=False,
            owner = curr_user
        ).order_by("arrive_time")
        completed_ride = Ride.objects.filter(
            confirmed=True,
            completed=True,
            owner = curr_user
        ).order_by("arrive_time")
        context = {"open_rides": open_ride,
                   "confirmed_rides": confirmed_ride,
                   "completed_rides": completed_ride,
                   "user":curr_user
                   }
        return render(request, 'dashboard/started_ride.html', context)

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/login')
    else:
        user_form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', context={'form': user_form,
                                                                  'profile_form': profile_form})

def ride_cancel(request, pk):
    if not request.session.get('is_login', None):
        return redirect('/login')
    ride = get_object_or_404(Ride, pk = pk)
    if not ride.owner == request.user:
        raise Http404
    ride.delete()

    return redirect('/')

def ride_detail(request, pk):
    if not request.session.get('is_login', None):
        return redirect('/login')
    gender = ['female', 'male', 'NG']
    vehicle_info = ['Sedan', 'SUV', 'Coupe', 'Hatchback', 'Mini van']
    ride = get_object_or_404(Ride, pk=pk)
    curr_user = get_object_or_404(User, id=request.session['user_id'])
    if curr_user != ride.owner:
        find = False
        groups = Group.objects.filter(user=request.user)
        for group in groups:
            if group in ride.shared_by_user.all():
                find = True
        if not find:
            raise Http404
    # status
    if ride.completed:
        status = "Completed"
    elif ride.confirmed:
        status = "Confirmed"
    else:
        status = "Open"
    # driver
    if ride.vehicle:
        driver = ride.vehicle.owner.first_name + ride.vehicle.owner.last_name
        plate = ride.vehicle.plateNumber
        driver_phone = ride.vehicle.owner.profile.mobile
        driver_email = ride.vehicle.owner.email
    else:
        driver = "Not assigned yet"
        plate = "Unknown"
        driver_phone = "Unknown"
        driver_email = "Unknown"

    shared_by = ride.shared_by_user.exclude(
        user=curr_user,
    )
    context = {
        "dest" : ride.dest,
        "arrive_time" : ride.arrive_time,
        "v_type": vehicle_info[ride.vehicleType],
        "shared_by": shared_by,
        "owner" : ride.owner,
        "status" : status,
        "driver" : driver,
        "plate" : plate,
        "driver_phone": driver_phone,
        "driver_Email": driver_email,
        "gender": gender,
        "curr_user": curr_user,
        "ride": ride
    }
    return render(request, 'dashboard/ride_detail.html',context)

class EditRide(SuccessMessageMixin, generic.UpdateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'dashboard/edit_ride.html'
    # redirect to this url after success
    success_url = "/"
    success_message = "Changes successfully saved."

    # Check if the user is qualified for edit
    def get_object(self, *args, **kwargs):
        if not self.request.session.get('is_login', None):
            return redirect('/login')
        ride = get_object_or_404(Ride, pk=self.kwargs['pk'])
        if not ride.owner == self.request.user:
            raise Http404
        return ride

def search_ride(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    if request.method == 'POST':
        form = SearchRide(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            #     vehicleType = cleaned_data.get('vehicleType')
            addr = cleaned_data.get('address')
            start = cleaned_data.get('start')
            end = cleaned_data.get('end')
            number = cleaned_data.get('passengerNum')

            # number = int(number)
            #format time
            start = start.astimezone(timezone.utc)
            end = end.astimezone(timezone.utc)

            rides = Ride.objects.filter(
                completed=False,
                confirmed=False,
                if_share=True,
                arrive_time__gte=start,
                arrive_time__lte=end
            ).exclude(owner=request.user).order_by("arrive_time")
            addr = str(addr).lower().split()
            groups = Group.objects.filter(user=request.user)
            for group in groups:
                rides = [ride for ride in rides if group not in ride.shared_by_user.all()]
            for word in addr:
                rides = [ride for ride in rides if word in str(ride.dest).lower()]
            rides = [ride for ride in rides if \
                     number + ride.get_passenger_num() + 1 <= \
                     ride.get_capacity()]
            rides.sort(key=lambda x: x.arrive_time)
            message = "{number} orders found: ".format(number = str(len(rides)))
        else:
            rides = []
            message = "Input invalid" + str(list(form.errors.values())[0])
    else:
        form = SearchRide(request.POST)
        rides = []
        message = "Results will be displayed below. "

    context = {
        "rides" : rides,
        "msg" : message,
        "form" : form
    }
    return render(request, 'dashboard/search_rides.html', context=context)

def join_ride(request, pk):
    if request.method == 'POST':
        ride = get_object_or_404(Ride, pk=pk)
        num_passengers = int(request.POST.get('number'))
        if num_passengers + ride.get_passenger_num() + 1 <= ride.get_capacity():
            try:
                group = Group.objects.get(user=request.user, groupNum=num_passengers)
            except Group.DoesNotExist:
                group = Group(user=request.user, groupNum=num_passengers)
                group.save()
            ride.shared_by_user.add(group)
            messages.success(request, 'Request successfully.')
            return redirect("/join_ride/success")
        else:
            return redirect("/join_ride/failed")

    return render(request, 'dashboard/join_ride.html')

def join_success(request):
    return render(request, 'dashboard/join_success.html')

def join_fail(request):
    return render(request, 'dashboard/join_failed.html')

def shared_rides(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    else:
        curr_user = get_object_or_404(User, id = request.session['user_id'])
        groups = Group.objects.filter(user=request.user)

        open_ride_ = Ride.objects.filter(
            confirmed=False,
            completed=False,
        ).exclude(owner=request.user).order_by("arrive_time")

        open_ride = []
        for group in groups:
            open_ride += [ride for ride in open_ride_ if group in ride.shared_by_user.all()]
        open_ride.sort(key=lambda x: x.arrive_time)

        confirmed_ride_ = Ride.objects.filter(
            confirmed=True,
            completed=False,
        ).exclude(owner=request.user).order_by("arrive_time")

        confirmed_ride = []
        for group in groups:
            confirmed_ride += [ride for ride in confirmed_ride_ if group in ride.shared_by_user.all()]
        confirmed_ride.sort(key=lambda x: x.arrive_time)

        completed_ride_ = Ride.objects.filter(
            confirmed=True,
            completed=True,
        ).exclude(owner=request.user).order_by("arrive_time")

        completed_ride = []
        for group in groups:
            completed_ride += [ride for ride in completed_ride_ if group in ride.shared_by_user.all()]
        completed_ride.sort(key=lambda x: x.arrive_time)

        context = {"open_rides": open_ride,
                   "confirmed_rides": confirmed_ride,
                   "completed_rides": completed_ride,
                   "user":curr_user
                   }
    return render(request, 'dashboard/shared_rides.html', context)

def quit_ride(request):
    return render(request, 'dashboard/join_failed.html')