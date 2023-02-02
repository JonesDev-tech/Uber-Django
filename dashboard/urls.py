from django.urls import path
from . import views

urlpatterns = [
    path('', views.started_ride, name='started_ride'),
    path('shared/', views.shared_rides, name='shared rides'),

    path('register/', views.register, name='register'),
    path('require_ride/', views.require_ride, name='require ride'),

    path('ride_detail/<int:pk>', views.ride_detail, name='ride detail'),
    path('ride_detail/<int:pk>/edit/', views.EditRide.as_view(), name='edit ride'),
    path('ride_detail/<int:pk>/cancel/', views.ride_cancel, name='cancel ride'),
    path('quit_ride/<int:pk>', views.quit_ride, name='quit ride'),

    path('search_rides/', views.search_ride, name='search rides'),
    path('join_ride/<int:pk>', views.join_ride, name='join ride'),
    path('join_ride/success', views.join_success, name='join success'),
    path('join_ride/failed', views.join_fail, name='join fail'),


    path('profile/', views.profile_page, name='profile'),
    path('profile/edit_personal_info', views.edit_profile, name='profile_edit_personal'),
    path('profile/change_credential', views.change_password, name='profile_edit_password'),


    path('driver/', views.test_url, name='test'),
    path('tasks/', views.test_url, name='test'),
    path('search_tasks/', views.test_url, name='test'),
    path('vehicles/', views.test_url, name='test'),
    #quit
    #vehicle registrate
    path('test/', views.test_url, name='test'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('post/new/', views.post_new, name='post_new'),
    #
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('post/<pk>/remove/', views.post_remove, name='post_remove'),

]