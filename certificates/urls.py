from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='certificates/index.html'),
        name='certificates-index'),
    # Endpoints
    url(r'^endpoints/$', views.endpoints, name='certificates-endpoints'),
    url(r'^endpoints/(?P<pk>[0-9]+)/$', views.endpoint,
        name='certificates-endpoint'),
    url(r'^endpoints/create/$', views.create_endpoint, name='certificates-create_endpoint'),
    url(r'^endpoints/scan/$', views.scan, name='certificates-scan'),

    # Dashboards
    url(r'^dashboard/expiring_soon/$', views.expiring_soon,
        name='certificates-expiring'),
]
