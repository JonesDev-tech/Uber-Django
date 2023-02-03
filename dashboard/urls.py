from django.urls import path
from . import views

urlpatterns = [
    path('', views.started_ride, name='started_ride'),
    path('shared/', views.shared_rides, name='shared rides'),

    path('register/', views.register, name='register'),
    path('require_ride/', views.require_ride, name='require ride'),

    path('ride_detail/<int:pk>', views.ride_detail, name='ride detail'),
    path('ride_detail/<int:pk>/edit/', views.EditRide.as_view(), name='edit ride'),
    # TODO: edit success
    path('ride_detail/<int:pk>/cancel/', views.ride_cancel, name='cancel ride'),
    path('quit_ride/<int:pk>', views.quit_ride, name='quit ride'),

    path('search_rides/', views.search_ride, name='search rides'),
    path('join_ride/<int:pk>', views.join_ride, name='join ride'),
    path('join_ride/success', views.join_success, name='join success'),
    path('join_ride/failed', views.join_fail, name='join fail'),


    path('profile/', views.profile_page, name='profile'),
    path('profile/edit_personal_info', views.edit_profile, name='profile_edit_personal'),
    path('profile/change_credential', views.change_password, name='profile_edit_password'),


    #vehicle registrate
    path('vehicle_reg/', views.vehicle_registrate, name='vehicle registrate'),
    #switch to driver portal redirect to vehicle regist or tasks
    path('driver/', views.switch_to_driver, name='switch to driver'),
    path('tasks/', views.driver_tasks, name='tasks'),

    path('search_tasks/', views.test_url, name='search tasks'),
    path('confirm/<int:pk>', views.test_url, name='search tasks'),

    path('my_vehicle/', views.test_url, name='my vehicle'),
    #delete driver account
    path('delete_account/', views.test_url, name='delete account'),

    path('test/', views.test_url, name='test'),

    path('404/', views.handle_404, name='404')
]