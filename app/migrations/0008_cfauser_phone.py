# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-21 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_cfauser_email_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="cfauser",
            name="phone",
            field=models.CharField(default="", max_length=15),
            preserve_default=False,
        ),
    ]
