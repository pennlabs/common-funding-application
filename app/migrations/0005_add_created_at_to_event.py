# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.created_at'
        db.add_column('app_event', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.created_at'
        db.delete_column('app_event', 'created_at')


    models = {
        'app.ccemail': {
            'Meta': {'object_name': 'CCEmail'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.cfauser': {
            'Meta': {'object_name': 'CFAUser'},
            'cc_emails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['app.CCEmail']", 'null': 'True', 'blank': 'True'}),
            'funder_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_statement': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'osa_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
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
            'advisor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'advisor_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'anticipated_attendance': ('django.db.models.fields.IntegerField', [], {}),
            'applied_funders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'event_applied_funders'", 'symmetrical': 'False', 'to': "orm['app.CFAUser']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'funding_already_received': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organizations': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_requester'", 'to': "orm['app.CFAUser']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
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
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2'}),
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