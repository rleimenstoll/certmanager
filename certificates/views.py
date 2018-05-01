# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import EndpointForm
from .models import Endpoint, Certificate, CertificateAssociation


@login_required
def endpoints(request):
    ctx = {}
    ctx['certificates'] = Certificate.objects.all()
    return render(request, 'certificates/endpoints.html', ctx)


@login_required
def create_endpoint(request):
    ctx = {}
    if request.method == 'POST':
        endpoint_form = EndpointForm(request.POST)
        if endpoint_form.is_valid():
            endpoint = endpoint_form.save()
            messages.success(request, 'Created endpoint %s' % endpoint)
            return redirect('certificates-create_endpoint')
    else:
        endpoint_form = EndpointForm()

    ctx['endpoint_form'] = endpoint_form
    return render(request, 'certificates/create_endpoint.html', ctx)


@login_required
def endpoint(request, pk):
    ctx = {}

    try:
        endpoint = Endpoint.objects.get(pk=pk)
    except Endpoint.DoesNotExist:
        raise Http404('Endpoint %s does not exist' % pk)

    ctx['endpoint'] = endpoint
    return render(request, 'certificates/endpoint.html', ctx)


@login_required
def scan(request):
    pass


@login_required
def expiring_soon(request):
    pass
# def scan(request):
#     ctx = {}
#     if request.method == 'POST':
#         endpoint_form = EndpointSelectForm(request.POST)
#         if endpoint_form.is_valid():
#             # Do something here
#             endpoint = endpoint_form.endpoint
#             messages.success(request, 'Created endpoint %s' % endpoint)
#             return redirect('certificates-create_endpoint')
#     else:
#         endpoint_form = EndpointSelectForm()
    #
    # ctx['endpoint_form'] = endpoint_form
    # return render(request, 'certificates/create_endpoint.html', ctx)
