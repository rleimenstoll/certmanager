from django.forms import ModelForm

from .models import Endpoint


class EndpointForm(ModelForm):

    class Meta:
        model = Endpoint
        exclude = ('active', 'certificates',)
