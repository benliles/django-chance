# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registration.created'
        db.add_column('chance_registration', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'EventChoiceOption.value'
        db.delete_column('chance_eventchoiceoption', 'value')

        # Adding field 'EventChoice.label'
        db.add_column('chance_eventchoice', 'label',
                      self.gf('django.db.models.fields.CharField')(default='label', max_length=255),
                      keep_default=False)


        # Changing field 'EventChoice.name'
        db.alter_column('chance_eventchoice', 'name', self.gf('django.db.models.fields.CharField')(max_length=32))
        # Adding unique constraint on 'EventChoice', fields ['name', 'event']
        db.create_unique('chance_eventchoice', ['name', 'event_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'EventChoice', fields ['name', 'event']
        db.delete_unique('chance_eventchoice', ['name', 'event_id'])

        # Deleting field 'Registration.created'
        db.delete_column('chance_registration', 'created')


        # User chose to not deal with backwards NULL issues for 'EventChoiceOption.value'
        raise RuntimeError("Cannot reverse this migration. 'EventChoiceOption.value' and its values cannot be restored.")
        # Deleting field 'EventChoice.label'
        db.delete_column('chance_eventchoice', 'label')


        # Changing field 'EventChoice.name'
        db.alter_column('chance_eventchoice', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'chance.event': {
            'Meta': {'object_name': 'Event'},
            'ends': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registration_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'starts': ('django.db.models.fields.DateTimeField', [], {})
        },
        'chance.eventchoice': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('name', 'event'),)", 'object_name': 'EventChoice'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['chance.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'chance.eventchoiceoption': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventChoiceOption'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['chance.EventChoice']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'chance.eventchoiceselection': {
            'Meta': {'object_name': 'EventChoiceSelection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['chance.EventChoiceOption']"}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': "orm['chance.Registration']"})
        },
        'chance.eventfee': {
            'Meta': {'object_name': 'EventFee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '255', 'decimal_places': '2'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fee_options'", 'to': "orm['chance.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'chance.registration': {
            'Meta': {'object_name': 'Registration'},
            'attendee_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'attendee_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['chance.Event']"}),
            'fee_option': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['chance.EventFee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['chance']