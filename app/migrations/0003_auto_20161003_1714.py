# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_auto_20160629_1552"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ccemail",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="cfauser",
            name="cc_emails",
            field=models.ManyToManyField(to="app.CCEmail", blank=True),
        ),
        migrations.AlterField(
            model_name="cfauser",
            name="osa_email",
            field=models.EmailField(
                help_text="The email address for contacting OSA when an app is funded.",
                max_length=254,
                null=True,
                verbose_name=b"OSA Contact Email",
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="advisor_email",
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="contact_email",
            field=models.EmailField(max_length=254),
        ),
    ]
