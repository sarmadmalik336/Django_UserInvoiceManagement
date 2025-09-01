from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Item
from django_countries.fields import CountryField

class InvoiceForm(forms.ModelForm):
    country = CountryField(default='IN')
    class Meta:
        model = Invoice
        fields = ['customer_name', 'email', 'gst_no', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country', 'gst', 'amount_paid', 'note']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'gst': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'gst_rate': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'all_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
        labels = {
            'customer_name': 'Company Name',
            'email': 'Company Email',
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_no', 'item_name', 'quantity', 'price']
        widgets = {
            'item_no': forms.TextInput(attrs={'class': 'form-control'}),
            'item_name': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'invoice': forms.Select(attrs={'class': 'form-control'}),
            'remove': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

ItemFormSet = inlineformset_factory(
    Invoice, Item, form=ItemForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
