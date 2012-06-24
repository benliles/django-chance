# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('chance_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('starts', self.gf('django.db.models.fields.DateTimeField')()),
            ('ends', self.gf('django.db.models.fields.DateTimeField')()),
            ('registration_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('chance', ['Event'])

        # Adding model 'EventFee'
        db.create_table('chance_eventfee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fee_options', to=orm['chance.Event'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=255, decimal_places=2)),
        ))
        db.send_create_signal('chance', ['EventFee'])

        # Adding model 'EventChoice'
        db.create_table('chance_eventchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['chance.Event'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('chance', ['EventChoice'])

        # Adding model 'EventChoiceOption'
        db.create_table('chance_eventchoiceoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['chance.EventChoice'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('chance', ['EventChoiceOption'])

        # Adding model 'Registration'
        db.create_table('chance_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registrations', to=orm['chance.Event'])),
            ('attendee_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('attendee_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('fee_option', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['chance.EventFee'])),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('chance', ['Registration'])

        # Adding model 'EventChoiceSelection'
        db.create_table('chance_eventchoiceselection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['chance.Registration'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['chance.EventChoiceOption'])),
        ))
        db.send_create_signal('chance', ['EventChoiceSelection'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('chance_event')

        # Deleting model 'EventFee'
        db.delete_table('chance_eventfee')

        # Deleting model 'EventChoice'
        db.delete_table('chance_eventchoice')

        # Deleting model 'EventChoiceOption'
        db.delete_table('chance_eventchoiceoption')

        # Deleting model 'Registration'
        db.delete_table('chance_registration')

        # Deleting model 'EventChoiceSelection'
        db.delete_table('chance_eventchoiceselection')


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
            'Meta': {'ordering': "('order',)", 'object_name': 'EventChoice'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['chance.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'chance.eventchoiceoption': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventChoiceOption'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['chance.EventChoice']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['chance.Event']"}),
            'fee_option': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['chance.EventFee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['chance']