# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import hashlib
import re

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding


from django.db import models


class CertificateAssociation(models.Model):

    endpoint = models.ForeignKey('endpoint')
    certificate = models.ForeignKey('certificate')

    date_added = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()

    def __unicode__(self):
        return u'Endpoint %s, Certificate %s' % (self.endpoint,
                                                 self.certificate)


class Endpoint(models.Model):

    name = models.CharField(max_length=64)
    host = models.CharField(max_length=256)
    port = models.IntegerField(default=443)
    active = models.BooleanField(default=True)

    certificates = \
        models.ManyToManyField('Certificate', through=CertificateAssociation)

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('host', 'port',)

    def __unicode__(self):
        return u'%s' % self.name

    @property
    def fingerprint(self):
        if self.certificate:
            return self.certificate.fingerprint

    @property
    def certificate(self):
        existing = \
            self.certificates.order_by('certificateassociation__last_seen')
        if existing.count() > 0:
            return existing[0]


class Certificate(models.Model):

    body = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    not_before = models.DateTimeField()
    not_after = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % self.pk

    @property
    def expired(self):
        return datetime.now() > self.not_after

    @property
    def fingerprint(self):
        # Attempt to parse certificate
        # TODO: Cache me!
        cert = load_pem_x509_certificate(str(self.body), default_backend())
        digest = hashlib.md5(cert.public_bytes(Encoding.DER)).hexdigest()
        return ':'.join(re.findall('..', digest))
