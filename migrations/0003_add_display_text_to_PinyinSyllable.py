# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from hanzi_basics.pinyin_nums_to_markers import pinyin_num_to_tone_marker

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Populating PinyinSyllable.display
        ps = orm['hanzi_basics.PinyinSyllable']
        missing_conversions = list()
        for s in ps.objects.all():
            try:
                s.display = pinyin_num_to_tone_marker[u'{}{}'.format(s.sound, s.tone)]
            except KeyError:
                missing_conversions.append('{}{}'.format(s.sound, s.tone))
                continue

            s.save()
        print(missing_conversions)

    def backwards(self, orm):
        
        ps = orm['hanzi_basics.pinyinsyllable']
        ps.objects.all().update(display='')

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
