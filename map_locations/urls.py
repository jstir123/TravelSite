from django.urls import path
from . import views
from django.contrib import admin

app_name = 'map_locations'

urlpatterns = [
    path('', views.HomeFeedView.as_view(), name='home'),
    path('mytrips/', views.MyTripsListView.as_view(), name='mytrips'),
    path('mytrips/new/', views.AddTripView.as_view(), name='trip_new'),
    path('mytrips/<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_edit'),
    path('mytrips/<int:pk>/remove/', views.TripDeleteView.as_view(), name='trip_delete'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('trips/<int:pk>/add_photos/', views.AddImageView.as_view(), name='add_image'),
    path('trips/<username>/', views.TripsListView.as_view(), name='trip_list'),
]
