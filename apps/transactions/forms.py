from django import forms

class TransferForm(forms.Form):
    recipient_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(min_value=0.01, decimal_places=2)
    note = forms.CharField(max_length=255, required=False)
