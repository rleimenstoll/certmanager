# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('not_before', models.DateTimeField()),
                ('not_after', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CertificateAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField()),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificates.Certificate')),
            ],
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('host', models.CharField(max_length=256)),
                ('port', models.IntegerField(default=443)),
                ('active', models.BooleanField(default=True)),
                ('certificates', models.ManyToManyField(through='certificates.CertificateAssociation', to='certificates.Certificate')),
            ],
        ),
        migrations.AddField(
            model_name='certificateassociation',
            name='endpoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificates.Endpoint'),
        ),
        migrations.AlterUniqueTogether(
            name='endpoint',
            unique_together=set([('host', 'port')]),
        ),
    ]