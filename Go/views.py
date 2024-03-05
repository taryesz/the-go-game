from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .decorators import redirect_authenticated_user
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .go_game.logic import proceed_game_logic


def welcome(request):
    return render(request, 'Go/welcome.html')


def proceed_authentication(request, form, password_type):

    username = form.cleaned_data['username']  # get the username
    password = form.cleaned_data[password_type]  # get the password

    user = authenticate(request, username=username, password=password)  # check the user

    if user is not None:  # if the user exists and confirmed:
        login(request, user)
        return redirect('profile', username=username)  # redirect to the user's profile page
    else:
        return HttpResponse('User does not exist')
        # TODO: inform that the user does not exist or login/pswd is not correct (flash message)


@login_required(login_url='login')
def log_user_out(request):
    logout(request)
    return redirect('/')


@redirect_authenticated_user
def log_user_in(request):

    # the login form is basically a normal form, but it inherits from AuthenticationForm

    # LOGIN FORM ===============================

    form = AuthenticationForm()  # create a blank form
    # or you can override this form (customize it) in forms.py

    if request.method == 'POST':  # if the form was submitted

        form = AuthenticationForm(request, request.POST)  # show the form with the input data

        if form.is_valid():
            return proceed_authentication(request, form, 'password')  # log the user in

    # ==========================================

    context = {
        'FORM': form,
    }

    return render(request, 'Go/login.html', context)


def log_user_up(request):

    # the registration form is basically a normal form, but it inherits from UserCreationForm

    # REGISTRATION FORM ========================

    form = CreateUser()  # create a blank form (that we overrode in forms.py)
    # or you can use the default django form [ form = UserCreationForm() ]

    if request.method == 'POST':  # if the form was submitted

        form = CreateUser(request.POST)  # show the form with the input data

        if form.is_valid():
            form.save()  # create the user
            return proceed_authentication(request, form, 'password1')  # and automatically log the user in

    # ==========================================

    context = {
        'FORM': form
    }

    return render(request, 'Go/signup.html', context)


@login_required(login_url='login')
def profile(request, username):

    user = Player.objects.get(username=username)  # get the user to whom this username belongs

    # CHECK IF USER'S PROFILE ==================

    if not request.user == user:
        # TODO: actually redirect to a login page, instead of staying on the user's profile
        return redirect('login')

    # STATS DATA ===============================

    stats = user.statistic_set.all()  # get the user's statistics
    played_games = stats.count()  # count the number of statistic records ~ the number of played games
    won_games = stats.filter(outcome='Victory').count()  # count the number of games won
    lost_games = stats.filter(outcome='Loss').count()  # count the number of games lost
    ties = stats.filter(outcome='Tie').count()  # count the number of games tied

    # FRIENDS LIST ==============================

    friends = user.friends_with.all()  # get all friends of user's

    # FRIENDS SEARCH ============================

    found_players = Player.objects.all()  # get all players in DB where we will have to look for our request
    search = FindFriend(request.GET, queryset=found_players)  # create filter, which will get data through GET
    found_players = search.qs  # apply the filter on all players, leave only those acceptable

    # GAME SETTINGS ============================

    game_form = GameSettings()

    # ADD FRIEND ===============================

    if request.method == 'POST':

        error_message = 'Oops, something went wrong'

        if 'add_friend' in request.POST:  # if a button that was pressed has a name 'action'
            friend_username = request.POST.get('add_friend')
            friend = Player.objects.get(username=friend_username)
            user.friends_with.add(friend)
            user.save()

            return redirect('profile', username=username)

        if 'remove_friend' in request.POST:
            friend_username = request.POST.get('remove_friend')
            friend = Player.objects.get(username=friend_username)
            user.friends_with.remove(friend)  # careful, don't confuse with .delete()
            user.save()

            return redirect('profile', username=username)

        if 'start_game' in request.POST:

            game_form = GameSettings(request.POST)

            if game_form.is_valid():

                game = game_form.save()

                game_id = game.id

                return redirect('play', username=username, game_id=game_id)

        return HttpResponse(error_message)

    # ==========================================

    context = {
        'USER': user,
        'PLAYS': played_games,
        'VICTORIES': won_games,
        'LOSSES': lost_games,
        'TIES': ties,
        'FILTER': search,
        'PLAYERS': found_players,
        'FRIENDS': friends,
        'GAME': game_form,
    }

    return render(request, 'Go/profile.html', context)


@login_required(login_url='login')
def settings(request, username):

    user = Player.objects.get(username=username)  # get the user to whom this username belongs

    # SETTINGS FORM ============================

    settings_form = Settings(instance=user)  # get the form we need to render and assign it to the user
    # NOTE: if we want to create a blank form (which would CREATE a new object, not UPDATE), don't pass the parameter

    if request.method == 'POST':

        error_message = 'Oops, something went wrong'

        if 'apply_settings' in request.POST:

            settings_form = Settings(request.POST, request.FILES, instance=user)  # request.FILES to handle images
            # fill new data as default for the form after submitting it

            if settings_form.is_valid():
                settings_form.save()
                username = settings_form.cleaned_data['username']
                return redirect(reverse('profile', args=[username]))

            # return HttpResponse(error_message)  TODO: replace this with a flash message

        if 'delete_user' in request.POST:

            settings_form = Settings(request.POST, instance=user)
            # fill new data as default for the form after submitting it

            if settings_form.is_valid():
                user.delete()
                return redirect('/')

            return HttpResponse(error_message)

        # return HttpResponse(error_message)

    # ==========================================

    context = {
        'USER': user,
        'FORM': settings_form
    }

    return render(request, 'Go/settings.html', context)


@login_required(login_url='login')
def play(request, username, game_id):

    game = Game.objects.get(id=game_id)

    user = Player.objects.get(username=username)

    if game.game_type == 'Versus':
        guest = Player.objects.get_or_create(
            first_name="Guest",
            last_name="Guest",
            username=str(game.id),
            email="guest.non-existent@mail.com",
        )[0]

        guest_stats = Statistic.objects.get_or_create(game=game, player=guest)[0]

    game_stats = Statistic.objects.get_or_create(game=game, player=user)[0]

    if request.method == 'POST':

        if 'stone' in request.POST:
            coordinates = request.POST.get('stone')
            x_coord, y_coord = coordinates.split("x")

            # Check if the stone exists at the coordinates
            if Stone.objects.filter(x_coord=x_coord, y_coord=y_coord, game=game).exists():
                pass  # TODO: flash message "Stone already exists"
            else:
                # Create a new stone
                new_stone = Stone.objects.create(x_coord=int(x_coord), y_coord=int(y_coord), game=game, color=not game_stats.last_move)

                # Update the turn
                game_stats.last_move = not game_stats.last_move
                game_stats.save()

                # LOGIC:
                proceed_game_logic(game, game_stats, guest_stats)

    stones = Stone.objects.filter(game=game)  # get all the game's stones and store as a list

    context = {
        'USER': user,
        'GAME': game,
        'BOARD': range(1, game.board_size + 1),
        'STATS': game_stats,
        'GUEST_STATS': guest_stats,
        'STONES': stones,
    }

    return render(request, 'Go/game.html', context)
