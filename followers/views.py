from django.views.generic import (View, DeleteView, ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Following

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class FollowerList(LoginRequiredMixin, ListView):
    template_name = 'followers/follower_list.html'
    model = Following

    def get_queryset(self):
        self.trip_user = User.objects.get(username__iexact=self.kwargs.get("username"))
        return Following.objects.filter(followed_user=self.trip_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_user'] = self.trip_user
        context['follow_list'] = Following.objects.filter(following_user=self.request.user).values()
        context['follow_list'] = [context['follow_list'][i]['followed_user_id'] for i in range(0, len(context['follow_list']))]
        return context


class FollowingList(LoginRequiredMixin, ListView):
    template_name = 'followers/following_list.html'
    model = Following

    def get_queryset(self):
        self.trip_user = User.objects.get(username__iexact=self.kwargs.get("username"))
        return Following.objects.filter(following_user=self.trip_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_user'] = self.trip_user
        context['follow_list'] = Following.objects.filter(following_user=self.request.user).values()
        context['follow_list'] = [context['follow_list'][i]['followed_user_id'] for i in range(0, len(context['follow_list']))]
        return context


# class FollowUser(View):
#     def get(self, request, *args, **kwargs):
#         self.trip_user = get_object_or_404(User, username=self.kwargs.get("username"))
#         # User.objects.get(username__iexact=self.kwargs.get("username"))
#         Following(following_user=request.user, followed_user=self.trip_user).save()
#         if self.kwargs.get("path") == 'userlist':
#             return HttpResponseRedirect('accounts/userlist/')
#         else:
#             return HttpResponseRedirect('map_locations/trips/{}/'.format(self.trip_user.username))

class FollowUser(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username=None, format=None):
        trip_user = get_object_or_404(User, username=username)
        Following(following_user=request.user, followed_user=trip_user).save()
        data = {
            "action": "follow",
            "username": username
        }
        return Response(data)


class UnfollowUser(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username=None, format=None):
        trip_user = get_object_or_404(User, username=username)
        Following.objects.filter(following_user=request.user, followed_user=trip_user).delete()
        data = {
            "action": "unfollow",
            "username": username
        }
        return Response(data)


# class UnfollowUser(View):
#     def get(self, request, *args, **kwargs):
#         self.trip_user = User.objects.get(username__iexact=self.kwargs.get("username"))
#         Following.objects.filter(following_user=request.user, followed_user=self.trip_user).delete()
#         if self.kwargs.get("path") == 'userlist':
#             return HttpResponseRedirect('accounts/userlist/')
#         else:
#             return HttpResponseRedirect('map_locations/trips/{}/'.format(self.trip_user.username))
