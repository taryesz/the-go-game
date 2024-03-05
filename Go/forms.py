from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Settings(ModelForm):

    class Meta:
        model = Player
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'username',
            'email',
            'dark_mode',
            'language',
        ]
        # fields = '__all__' - to select every field


class CreateUser(UserCreationForm):  # inherit from UserCreationForm to get all the functionality

    class Meta:         # change settings here:
        model = Player  # we could also use the default django User model (model=User), but we want our custom one
        fields = [      # specify what fields to show
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]


class GameSettings(ModelForm):

    class Meta:
        model = Game
        fields = [
            'board_size',
            'game_type',
            'start_with_color',
        ]
