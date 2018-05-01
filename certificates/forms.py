from django.forms import ModelForm, Form, ModelChoiceField

from .models import Endpoint


class EndpointForm(ModelForm):

    class Meta:
        model = Endpoint
        exclude = ('active', 'certificates',)


class EndpointSelectForm(Form):
    endpoint = ModelChoiceField(queryset=Endpoint.objects.all())
