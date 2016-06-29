# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CCEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CFAUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('funder_name', models.CharField(default=b'', max_length=256, blank=True)),
                ('user_type', models.CharField(max_length=1, choices=[(b'R', b'REQUESTER'), (b'F', b'FUNDER')])),
                ('osa_email', models.EmailField(help_text=b'The email address for contacting OSA when an app is funded.', max_length=75, null=True, verbose_name=b'OSA Contact Email', blank=True)),
                ('mission_statement', models.TextField(max_length=256, blank=True)),
                ('cc_emails', models.ManyToManyField(to='app.CCEmail', null=True, blank=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL, help_text=b'You must first create a user before adding them to the CFA.')),
            ],
            options={
                'verbose_name': 'CFA Users',
                'verbose_name_plural': 'CFA Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonFollowupAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonFollowupQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonFreeResponseAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonFreeResponseQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EligibilityAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1, choices=[(b'Y', b'YES'), (b'N', b'NO')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EligibilityQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=256)),
                ('contact_name', models.CharField(max_length=256, blank=True)),
                ('contact_email', models.EmailField(max_length=75)),
                ('contact_phone', models.CharField(max_length=15)),
                ('anticipated_attendance', models.IntegerField()),
                ('advisor_email', models.EmailField(max_length=75, blank=True)),
                ('advisor_phone', models.CharField(max_length=15, blank=True)),
                ('organizations', models.CharField(max_length=256)),
                ('funding_already_received', models.DecimalField(default=0, max_digits=17, decimal_places=2)),
                ('status', models.CharField(max_length=1, choices=[(b'S', b'SAVED'), (b'B', b'SUBMITTED'), (b'F', b'FUNDED'), (b'W', b'FOLLOWUP'), (b'O', b'OVER')])),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('applied_funders', models.ManyToManyField(related_name=b'event_applied_funders', to='app.CFAUser')),
                ('requester', models.ForeignKey(related_name=b'event_requester', to='app.CFAUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowupAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
                ('event', models.ForeignKey(to='app.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowupQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('funder', models.ForeignKey(to='app.CFAUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FreeResponseAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
                ('event', models.ForeignKey(to='app.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FreeResponseQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('funder', models.ForeignKey(to='app.CFAUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FunderConstraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1, choices=[(b'Y', b'YES'), (b'N', b'NO')])),
                ('funder', models.ForeignKey(to='app.CFAUser')),
                ('question', models.ForeignKey(to='app.EligibilityQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
                ('funder', models.ForeignKey(to='app.CFAUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('quantity', models.IntegerField()),
                ('price_per_unit', models.DecimalField(max_digits=17, decimal_places=2)),
                ('funding_already_received', models.DecimalField(max_digits=17, decimal_places=2)),
                ('category', models.CharField(max_length=1, choices=[(b'H', b'Honoraria/Services'), (b'E', b'Equipment/Supplies'), (b'F', b'Food/Drinks'), (b'S', b'Facilities/Security'), (b'T', b'Travel/Conference'), (b'P', b'Photocopies/Printing/Publicity'), (b'O', b'Other')])),
                ('revenue', models.BooleanField()),
                ('event', models.ForeignKey(to='app.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grant',
            name='item',
            field=models.ForeignKey(to='app.Item'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grant',
            unique_together=set([('funder', 'item')]),
        ),
        migrations.AlterUniqueTogether(
            name='funderconstraint',
            unique_together=set([('funder', 'question')]),
        ),
        migrations.AddField(
            model_name='freeresponseanswer',
            name='question',
            field=models.ForeignKey(to='app.FreeResponseQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='followupanswer',
            name='question',
            field=models.ForeignKey(to='app.FollowupQuestion'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('name', 'date', 'requester')]),
        ),
        migrations.AddField(
            model_name='eligibilityanswer',
            name='event',
            field=models.ForeignKey(to='app.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eligibilityanswer',
            name='question',
            field=models.ForeignKey(to='app.EligibilityQuestion'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='eligibilityanswer',
            unique_together=set([('question', 'event', 'answer')]),
        ),
        migrations.AddField(
            model_name='commonfreeresponseanswer',
            name='event',
            field=models.ForeignKey(to='app.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonfreeresponseanswer',
            name='question',
            field=models.ForeignKey(to='app.CommonFreeResponseQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonfollowupanswer',
            name='event',
            field=models.ForeignKey(to='app.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commonfollowupanswer',
            name='question',
            field=models.ForeignKey(to='app.CommonFollowupQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(to='app.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='funder',
            field=models.ForeignKey(to='app.CFAUser'),
            preserve_default=True,
        ),
    ]
