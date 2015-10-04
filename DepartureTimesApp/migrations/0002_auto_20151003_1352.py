# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DepartureTimesApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('agency_tag', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('regionTitle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Busstop',
            fields=[
                ('stop_tag', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('stopId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('direction_tag', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('route_tag', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('agency', models.ForeignKey(to='DepartureTimesApp.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.ForeignKey(to='DepartureTimesApp.Direction')),
                ('stop', models.ForeignKey(to='DepartureTimesApp.Busstop')),
            ],
        ),
        migrations.AddField(
            model_name='direction',
            name='route',
            field=models.ForeignKey(to='DepartureTimesApp.Route'),
        ),
    ]
