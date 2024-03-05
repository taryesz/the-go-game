from django.shortcuts import redirect


def redirect_authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # if a logged-in user tries to access an account (theirs or someone else's):
            return redirect('profile', request.user)
        else:  # if a non-logged-in user tries to access an account
            return view_func(request, *args, **kwargs)  # proceed to signing in
    return wrapper_func

#
# def turn(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.
#
#         return view_func(request, **args, **kwargs)
#     return wrapper_func

# only users that are in "Group" can have access to some pages - right now though i don't need this functionality
# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             return view_func(request, *args, **kwargs)
#         return wrapper_func
#     return decorator

