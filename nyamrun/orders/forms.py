from django import forms
from places.models import Address


class OrderForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), label="Адрес заведения")
    time = forms.TimeField(
        label="Время приготовления",
        widget=forms.TimeInput(attrs={
            'type': 'time', 'min': '08:00', 'max': '22:00', 'step': '900'
        })
    )
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Комментарий")

    def __init__(self, *args, **kwargs):
        place = kwargs.pop('place', None)
        super().__init__(*args, **kwargs)
        if place:
            self.fields['address'].queryset = place.addresses.all()
        else:
            self.fields['address'].queryset = Address.objects.all()[:0]
