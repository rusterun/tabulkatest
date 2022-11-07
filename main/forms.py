from .models import Bookings, Properties
from django.forms import Form, ModelForm, TextInput, SelectDateWidget, ModelChoiceField

class BookingsForm(ModelForm):
    class Meta:
        model = Bookings
        property = ModelChoiceField(queryset=Properties.objects.all())
        fields = ['property', 'first_name', 'last_name', 'arrival', 'departure']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'arrival': SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
            'departure': SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
        }

