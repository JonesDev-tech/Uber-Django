from django.shortcuts import get_object_or_404, redirect, render, render
from .forms import RegisterForm, ProfileForm, RideRequestForm
from .models import User, Profile, Ride, Group
# from django.urls import reverse
# from django.utils import timezone
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from .backend import VehicleInfo

def require_ride(request):
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
def ride_edit(request, pk):
    return
def ride_cancel(request, pk):
    return

def ride_detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    curr_user = get_object_or_404(User, id=request.session['user_id'])
    # vehicle_info = VehicleInfo()
    if curr_user != ride.owner:
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

    owner = ride.shared_by_user.get(
        user=curr_user
    )
    shared_by = ride.shared_by_user.exclude(
        user=curr_user,
    )
    context = {
        "dest" : ride.dest,
        "arrive_time" : ride.arrive_time,
        "v_type": ride.vehicleType,
        "shared_by": shared_by,
        "owner" : owner,
        "status" : status,
        "driver" : driver,
        "plate" : plate,
        "driver_phone": driver_phone,
        "driver_Email": driver_email,
    }
    return render(request, 'registration/register.html',context)