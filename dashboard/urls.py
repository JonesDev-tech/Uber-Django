from django.urls import path
from . import views

urlpatterns = [
    path('', views.started_ride, name='started_ride'),
    path('register/', views.register, name='register'),
    path('require_ride/', views.require_ride, name='require ride'),
    path('ride_detail/<int:pk>', views.ride_detail, name='ride detail'),
    path('ride_detail/<int:pk>/edit/', views.EditRide.as_view(), name='edit ride'),
    path('ride_detail/<int:pk>/cancel/', views.ride_cancel, name='cancel ride'),

    path('search_rides/', views.search_ride, name='search rides'),
    path('join_ride/<int:pk>', views.search_ride, name='join ride'),
    path('quit_ride/<int:pk>', views.search_ride, name='quit ride'),

    path('profile/', views.ride_cancel, name='profile'),
    path('profile/edit_personal_info', views.ride_cancel, name='profile_edit_personal'),
    path('profile/change_credential', views.ride_cancel, name='profile_edit_password'),
    # path('register/', views.register, name='register'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('post/new/', views.post_new, name='post_new'),
    #
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('post/<pk>/remove/', views.post_remove, name='post_remove'),

]