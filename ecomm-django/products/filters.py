import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    from_price = django_filters.NumberFilter(field_name='price', label='Price from:', lookup_expr='gte')
    to_price = django_filters.NumberFilter(field_name='price', label='Price to:', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ()
