from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .poll import poll


@shared_task
def trigger_poll(pk):
    '''Initiate a poll of a given endpoint with primary key pk.'''
    poll(pk)
