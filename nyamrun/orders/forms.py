from django import forms

from orders.models import Order
from places.models import Address


class OrderForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(), label="Адрес заведения"
    )
    time = forms.ChoiceField(label="Время приготовления", choices=[])
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Например: без лука", "class": "comment-field"}
        ),
        required=False,
        label="Комментарий",
    )

    def __init__(self, *args, **kwargs):
        place = kwargs.pop("place", None)
        time_choices = kwargs.pop("time_choices", None)
        super().__init__(*args, **kwargs)
        if place:
            self.fields["address"].queryset = place.addresses.all()
        else:
            self.fields["address"].queryset = Address.objects.all()[:0]

        if time_choices:
            self.fields["time"].choices = time_choices
        else:
            from .views import get_time_choices

            self.fields["time"].choices = get_time_choices()


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "order-status-select"}),
        }
