# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-18 20:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='liked_users',
        ),
        migrations.RemoveField(
            model_name='books',
            name='uploader',
        ),
        migrations.DeleteModel(
            name='books',
        ),
    ]