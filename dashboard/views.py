from django.shortcuts import get_object_or_404, redirect, render, render
# from .forms import RegisterForm, PostForm
from django.urls import reverse
from django.utils import timezone
# from .models import Post, about
from django.contrib.auth.models import User
from django.http import Http404
#import markdown
import re

def dashboard(request):
    # posts = Post.objects.filter(
    #     published_date__lte=timezone.now()).order_by('published_date')
    # about_ = about.objects.all()
    return render(request, 'dashboard/homepage.html', {})