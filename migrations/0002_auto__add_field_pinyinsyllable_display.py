# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PinyinSyllable.display'
        db.add_column('hanzi_basics_pinyinsyllable', 'display', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PinyinSyllable.display'
        db.delete_column('hanzi_basics_pinyinsyllable', 'display')


    models = {
        'hanzi_basics.hanzi': {
            'Meta': {'object_name': 'Hanzi'},
            'char': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'syllables': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hanzi_basics.PinyinSyllable']", 'symmetrical': 'False'}),
            'use_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'hanzi_basics.pinyinsyllable': {
            'Meta': {'object_name': 'PinyinSyllable'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sound': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tone': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hanzi_basics']
