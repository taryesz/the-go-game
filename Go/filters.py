import django_filters
from .models import *
from django_filters import DateFilter, CharFilter


class FindFriend(django_filters.FilterSet):

    # create an input field to look up a player by their nickname (dynamically)
    username = CharFilter(field_name='username', lookup_expr='icontains', label="Find people:")

    # you can also add date filter:
    # start = DateFilter(field_name='date_joined', lookup_expr='gte')

    class Meta:
        model = Player
        fields = ['username']
        exclude = ['username']  # you have to exclude a field to be able to customize it with a django_filter ^
