from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import ProfilePicture


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("first_name","last_name","username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email Address"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"


class ProfilePicForm(forms.ModelForm):

    class Meta:
        fields = ("prof_pic",)
        model = ProfilePicture

        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }
