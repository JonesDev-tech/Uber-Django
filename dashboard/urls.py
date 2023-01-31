from django.urls import path
from . import views

urlpatterns = [
    path('', views.started_ride, name='started_ride'),
    path('register/', views.register, name='register'),
    path('require_ride/', views.require_ride, name='require ride'),
    # path('register/', views.register, name='register'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('post/new/', views.post_new, name='post_new'),
    #
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('post/<pk>/remove/', views.post_remove, name='post_remove'),

]