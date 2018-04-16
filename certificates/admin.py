# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Endpoint, Certificate, CertificateAssociation


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    pass


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    pass


@admin.register(CertificateAssociation)
class CertificateAssociationAdmin(admin.ModelAdmin):
    pass
