# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailTemplate'
        db.create_table(u'dbmail_mailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('plain_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('html_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dbmail', ['MailTemplate'])


    def backwards(self, orm):
        # Deleting model 'MailTemplate'
        db.delete_table(u'dbmail_mailtemplate')


    models = {
        u'dbmail.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'html_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plain_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['dbmail']