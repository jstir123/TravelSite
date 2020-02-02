from django.contrib.auth import (login, logout, get_user_model)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms, models
from django.contrib import auth
from followers.models import Following
from django.db.models import Q

User = get_user_model()

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


class UserListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/user_list.html'
    model = User

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query == '':
            return super().get_queryset()
        else:
            user_list = get_user_queryset(query)
            return User.objects.filter(id__in=[u.id for u in user_list])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following_list'] = Following.objects.filter(following_user=self.request.user)
        context['following_list'] = [i.followed_user.id for i in context['following_list']]
        return context


class AddProfilePicture(LoginRequiredMixin, CreateView):
    template_name = 'accounts/profilepicture_form.html'
    form_class = forms.ProfilePicForm
    success_url = reverse_lazy('map_locations:mytrips')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateProfilePicture(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profilepicture_form.html'
    form_class = forms.ProfilePicForm
    model = models.ProfilePicture
    success_url = reverse_lazy('map_locations:mytrips')


#Function to define query from search input
def get_user_queryset(query=None):
    queryset = []
    queries = query.split(' ')

    for q in queries:
        users = User.objects.filter(
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q)
            ).distinct()

        for u in users:
            queryset.append(u)

    return list(set(queryset))
