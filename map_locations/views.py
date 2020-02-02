from django.views.generic import (CreateView, ListView, DetailView, UpdateView,
                                  DeleteView, FormView)
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from map_locations.models import Trips, TripImages
from followers.models import Following
from map_locations.forms import TripForm, UpdateTripForm, TripImageForm
from django.db.models import Q
from pycountry import countries

import googlemaps

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
gmaps = googlemaps.Client(key='AIzaSyCTjVXl881QGgXNpO5Vfidv_Tu-62v8N-I')


class HomeFeedView(LoginRequiredMixin, ListView):
    template_name = 'map_locations/home.html'
    model = Trips

    def get_queryset(self):
        self.following_list = Following.objects.filter(following_user=self.request.user)
        self.following_list = [i.followed_user.id for i in self.following_list]
        self.location = self.request.GET.get('loc_q', 'All')

        if self.location == 'All':
            return Trips.objects.filter(traveler_id__in=self.following_list)
        else:
            return get_trip_queryset(self.location, self.following_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loc_filter_list'] = list(set([str(i) for i in Trips.objects.filter(traveler_id__in=self.following_list)]))
        context['loc_filter_list'].sort()
        context['selected_loc_filter'] = self.location
        return context

class MyTripsListView(LoginRequiredMixin, ListView):
    template_name = 'map_locations/my_trips_list.html'
    model = Trips

    def get_queryset(self):
        return Trips.objects.filter(traveler=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following_count'] = len(Following.objects.filter(following_user=self.request.user))
        context['follower_count'] = len(Following.objects.filter(followed_user=self.request.user))
        return context


class TripsListView(LoginRequiredMixin, ListView):
    model = Trips

    def get_queryset(self):
        try:
            self.trip_user = User.objects.prefetch_related('user_trips').get(
                username__iexact=self.kwargs.get('username'))

        except User.DoesNotExist:
            raise Http404

        else:
            return self.trip_user.user_trips.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_user'] = self.trip_user
        context['following_list'] = Following.objects.filter(following_user=self.request.user)
        context['following_list'] = [i.followed_user.id for i in context['following_list']]
        context['following_count'] = len(Following.objects.filter(following_user=self.trip_user))
        context['follower_count'] = len(Following.objects.filter(followed_user=self.trip_user))
        return context


class AddTripView(LoginRequiredMixin, CreateView):
    redirect_field_name = 'map_locations/my_trips_list.html'
    form_class = TripForm
    model = Trips

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.city = self.object.city.title()
        to_geocode = str(self.object)
        geocode_result = gmaps.geocode(to_geocode)
        self.object.latitude = geocode_result[0]['geometry']['location']['lat']
        self.object.longitude = geocode_result[0]['geometry']['location']['lng']
        self.object.traveler = self.request.user
        self.object.save()
        return super().form_valid(form)


class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trips


class TripUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'map_locations/trips_update_form.html'
    redirect_field_name = 'map_locations/trip_detail.html'
    form_class = UpdateTripForm
    model = Trips


class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trips
    success_url = reverse_lazy('map_locations:mytrips')


class AddImageView(LoginRequiredMixin, FormView):
    form_class = TripImageForm
    template_name = 'map_locations/tripimages_form.html'

    def get_success_url(self):
        return reverse('map_locations:trip_detail', kwargs={'pk':self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        if form.is_valid():
            return self.form_valid(form, files)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, files):
        for f in files:
            self.trip_id = Trips.objects.get(pk=self.kwargs.get('pk'))
            TripImages.objects.create(trip=self.trip_id, image=f)
        return super().form_valid(form)


#Function to define query based on location filter
def get_trip_queryset(loc=None, id_list=None):
    city = loc.split(',')[0]
    state_country = loc.split(', ')[1]
    if len(state_country) > 2:
        state_country = countries.get(name=state_country).alpha_2

    criteria = Q(traveler_id__in=id_list) & (
               Q(city__icontains=city) & (
               Q(state__icontains=state_country) | Q(country__icontains=state_country)))
    return Trips.objects.filter(criteria)
