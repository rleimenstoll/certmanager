# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


class CertificateAssociation(models.Model):

    endpoint = models.ForeignKey('endpoint')
    certificate = models.ForeignKey('certificate')

    date_added = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()

    def __unicode__(self):
        u'Endpoint %s, Certificate %s' % (self.endpoint, self.certificate)


class Endpoint(models.Model):

    name = models.CharField(max_length=64)
    host = models.CharField(max_length=256)
    port = models.IntegerField(default=443)
    active = models.BooleanField(default=True)

    certificates = models.ManyToManyField('Certificate', through=CertificateAssociation)


    class Meta:
        unique_together = ('host', 'port',)

    def __unicode__(self):
        return u'%s' % name


class Certificate(models.Model):

    body = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    not_before = models.DateTimeField()
    not_after = models.DateTimeField()

    @property
    def expired(self):
        return datetime.now() > self.not_after
