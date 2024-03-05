from django.http import Http404


def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper



