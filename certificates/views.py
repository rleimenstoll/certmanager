# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import EndpointForm, EndpointSelectForm
from .models import Endpoint, Certificate, CertificateAssociation
from .tasks import trigger_poll


@login_required
def endpoints(request):
    ctx = {}
    ctx['endpoints'] = Endpoint.objects.all()
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
def expiring_soon(request):
    pass


@login_required
def scan(request):
    ctx = {}
    if request.method == 'POST':
        endpoint_form = EndpointSelectForm(request.POST)
        if endpoint_form.is_valid():
            # Do something here
            endpoint = endpoint_form.cleaned_data['endpoint']
            trigger_poll.delay(pk=endpoint.pk)
            messages.info(request, 'Scan for %s started.' % endpoint)
            return redirect('certificates-scan')
    else:
        endpoint_form = EndpointSelectForm()

    ctx['endpoint_form'] = endpoint_form
    return render(request, 'certificates/trigger_scan.html', ctx)
