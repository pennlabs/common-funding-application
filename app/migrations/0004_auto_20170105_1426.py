# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20161003_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfauser',
            name='mission_statement',
            field=models.TextField(blank=True),
        ),
    ]
