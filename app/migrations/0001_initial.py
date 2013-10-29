# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CFAUser'
        db.create_table('app_cfauser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('osa_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('mission_statement', self.gf('django.db.models.fields.TextField')(max_length=256)),
        ))
        db.send_create_signal('app', ['CFAUser'])

        # Adding model 'Event'
        db.create_table('app_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_requester', to=orm['app.CFAUser'])),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('anticipated_attendance', self.gf('django.db.models.fields.IntegerField')()),
            ('admission_fee', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('advisor_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('advisor_phone', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('organizations', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('funding_already_received', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=2)),
            ('over', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Event'])

        # Adding unique constraint on 'Event', fields ['name', 'date', 'requester']
        db.create_unique('app_event', ['name', 'date', 'requester_id'])

        # Adding M2M table for field applied_funders on 'Event'
        db.create_table('app_event_applied_funders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['app.event'], null=False)),
            ('cfauser', models.ForeignKey(orm['app.cfauser'], null=False))
        ))
        db.create_unique('app_event_applied_funders', ['event_id', 'cfauser_id'])

        # Adding model 'Comment'
        db.create_table('app_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CFAUser'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('app', ['Comment'])

        # Adding model 'EligibilityQuestion'
        db.create_table('app_eligibilityquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['EligibilityQuestion'])

        # Adding model 'EligibilityAnswer'
        db.create_table('app_eligibilityanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.EligibilityQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('app', ['EligibilityAnswer'])

        # Adding unique constraint on 'EligibilityAnswer', fields ['question', 'event', 'answer']
        db.create_unique('app_eligibilityanswer', ['question_id', 'event_id', 'answer'])

        # Adding model 'CommonFollowupQuestion'
        db.create_table('app_commonfollowupquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['CommonFollowupQuestion'])

        # Adding model 'CommonFollowupAnswer'
        db.create_table('app_commonfollowupanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CommonFollowupQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['CommonFollowupAnswer'])

        # Adding model 'FollowupQuestion'
        db.create_table('app_followupquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('funder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CFAUser'])),
        ))
        db.send_create_signal('app', ['FollowupQuestion'])

        # Adding model 'FollowupAnswer'
        db.create_table('app_followupanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.FollowupQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['FollowupAnswer'])

        # Adding model 'CommonFreeResponseQuestion'
        db.create_table('app_commonfreeresponsequestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['CommonFreeResponseQuestion'])

        # Adding model 'CommonFreeResponseAnswer'
        db.create_table('app_commonfreeresponseanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CommonFreeResponseQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['CommonFreeResponseAnswer'])

        # Adding model 'FreeResponseQuestion'
        db.create_table('app_freeresponsequestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('funder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CFAUser'])),
        ))
        db.send_create_signal('app', ['FreeResponseQuestion'])

        # Adding model 'FreeResponseAnswer'
        db.create_table('app_freeresponseanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.FreeResponseQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['FreeResponseAnswer'])

        # Adding model 'Item'
        db.create_table('app_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('price_per_unit', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=2)),
            ('funding_already_received', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=2)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('revenue', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Item'])

        # Adding model 'Grant'
        db.create_table('app_grant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CFAUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Item'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=2)),
        ))
        db.send_create_signal('app', ['Grant'])

        # Adding unique constraint on 'Grant', fields ['funder', 'item']
        db.create_unique('app_grant', ['funder_id', 'item_id'])

        # Adding model 'FunderConstraint'
        db.create_table('app_funderconstraint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('funder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CFAUser'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.EligibilityQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('app', ['FunderConstraint'])

        # Adding unique constraint on 'FunderConstraint', fields ['funder', 'question']
        db.create_unique('app_funderconstraint', ['funder_id', 'question_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FunderConstraint', fields ['funder', 'question']
        db.delete_unique('app_funderconstraint', ['funder_id', 'question_id'])

        # Removing unique constraint on 'Grant', fields ['funder', 'item']
        db.delete_unique('app_grant', ['funder_id', 'item_id'])

        # Removing unique constraint on 'EligibilityAnswer', fields ['question', 'event', 'answer']
        db.delete_unique('app_eligibilityanswer', ['question_id', 'event_id', 'answer'])

        # Removing unique constraint on 'Event', fields ['name', 'date', 'requester']
        db.delete_unique('app_event', ['name', 'date', 'requester_id'])

        # Deleting model 'CFAUser'
        db.delete_table('app_cfauser')

        # Deleting model 'Event'
        db.delete_table('app_event')

        # Removing M2M table for field applied_funders on 'Event'
        db.delete_table('app_event_applied_funders')

        # Deleting model 'Comment'
        db.delete_table('app_comment')

        # Deleting model 'EligibilityQuestion'
        db.delete_table('app_eligibilityquestion')

        # Deleting model 'EligibilityAnswer'
        db.delete_table('app_eligibilityanswer')

        # Deleting model 'CommonFollowupQuestion'
        db.delete_table('app_commonfollowupquestion')

        # Deleting model 'CommonFollowupAnswer'
        db.delete_table('app_commonfollowupanswer')

        # Deleting model 'FollowupQuestion'
        db.delete_table('app_followupquestion')

        # Deleting model 'FollowupAnswer'
        db.delete_table('app_followupanswer')

        # Deleting model 'CommonFreeResponseQuestion'
        db.delete_table('app_commonfreeresponsequestion')

        # Deleting model 'CommonFreeResponseAnswer'
        db.delete_table('app_commonfreeresponseanswer')

        # Deleting model 'FreeResponseQuestion'
        db.delete_table('app_freeresponsequestion')

        # Deleting model 'FreeResponseAnswer'
        db.delete_table('app_freeresponseanswer')

        # Deleting model 'Item'
        db.delete_table('app_item')

        # Deleting model 'Grant'
        db.delete_table('app_grant')

        # Deleting model 'FunderConstraint'
        db.delete_table('app_funderconstraint')


    models = {
        'app.cfauser': {
            'Meta': {'object_name': 'CFAUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_statement': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'osa_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'app.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'funder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CFAUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.commonfollowupanswer': {
            'Meta': {'object_name': 'CommonFollowupAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CommonFollowupQuestion']"})
        },
        'app.commonfollowupquestion': {
            'Meta': {'object_name': 'CommonFollowupQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'app.commonfreeresponseanswer': {
            'Meta': {'object_name': 'CommonFreeResponseAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CommonFreeResponseQuestion']"})
        },
        'app.commonfreeresponsequestion': {
            'Meta': {'object_name': 'CommonFreeResponseQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'app.eligibilityanswer': {
            'Meta': {'unique_together': "(('question', 'event', 'answer'),)", 'object_name': 'EligibilityAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.EligibilityQuestion']"})
        },
        'app.eligibilityquestion': {
            'Meta': {'object_name': 'EligibilityQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'app.event': {
            'Meta': {'unique_together': "(('name', 'date', 'requester'),)", 'object_name': 'Event'},
            'admission_fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'advisor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'advisor_phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'anticipated_attendance': ('django.db.models.fields.IntegerField', [], {}),
            'applied_funders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'event_applied_funders'", 'symmetrical': 'False', 'to': "orm['app.CFAUser']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'funding_already_received': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organizations': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'over': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_requester'", 'to': "orm['app.CFAUser']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        'app.followupanswer': {
            'Meta': {'object_name': 'FollowupAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.FollowupQuestion']"})
        },
        'app.followupquestion': {
            'Meta': {'object_name': 'FollowupQuestion'},
            'funder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CFAUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'app.freeresponseanswer': {
            'Meta': {'object_name': 'FreeResponseAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.FreeResponseQuestion']"})
        },
        'app.freeresponsequestion': {
            'Meta': {'object_name': 'FreeResponseQuestion'},
            'funder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CFAUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'app.funderconstraint': {
            'Meta': {'unique_together': "(('funder', 'question'),)", 'object_name': 'FunderConstraint'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'funder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CFAUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.EligibilityQuestion']"})
        },
        'app.grant': {
            'Meta': {'unique_together': "(('funder', 'item'),)", 'object_name': 'Grant'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'funder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CFAUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Item']"})
        },
        'app.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            'funding_already_received': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'price_per_unit': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'revenue': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']