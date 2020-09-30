from django import forms
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street = forms.CharField()
    internal_number = forms.CharField(required=False)
    external_number = forms.CharField()
    suburb = forms.CharField()
    city = forms.CharField()
    # country = CountryField(blank_label='Select Country').formfield()
    country = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    phone_number = forms.CharField()

    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
