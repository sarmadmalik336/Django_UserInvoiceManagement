import django_filters
from django import forms
from .models import User, Invoice

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search Username:'}),
        label='',
    )

    class Meta:
        model = User
        fields = ['name']

class InvoiceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search Company Name'}),
        label='',
    )
    created_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'placeholder': 'Select User'}),
        label='',
        field_name='created_by__name',
        empty_label='--- Select User ---',
    )

    class Meta:
        model = Invoice
        fields = ['created_by', 'customer_name']

class InvoiceUserFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search Company Name'}),
        label='',
    )

    class Meta:
        model = Invoice
        fields = ['customer_name']