from django.shortcuts import get_object_or_404, redirect, render, render
from .forms import RegisterForm, ProfileForm
# from django.urls import reverse
# from django.utils import timezone
# # from .models import Post, about
# from django.contrib.auth.models import User
# from django.http import Http404
# #import markdown
# import re

def started_ride(request):
    if not request.session.get('is_login', None):
        return redirect('/login')
    else:

        return render(request, 'dashboard/started_ride.html', {})

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