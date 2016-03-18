# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PinyinSyllable'
        db.create_table('hanzi_basics_pinyinsyllable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sound', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tone', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hanzi_basics', ['PinyinSyllable'])

        # Adding model 'Hanzi'
        db.create_table('hanzi_basics_hanzi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('char', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1)),
            ('use_rank', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('hanzi_basics', ['Hanzi'])

        # Adding M2M table for field syllables on 'Hanzi'
        db.create_table('hanzi_basics_hanzi_syllables', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hanzi', models.ForeignKey(orm['hanzi_basics.hanzi'], null=False)),
            ('pinyinsyllable', models.ForeignKey(orm['hanzi_basics.pinyinsyllable'], null=False))
        ))
        db.create_unique('hanzi_basics_hanzi_syllables', ['hanzi_id', 'pinyinsyllable_id'])


    def backwards(self, orm):
        
        # Deleting model 'PinyinSyllable'
        db.delete_table('hanzi_basics_pinyinsyllable')

        # Deleting model 'Hanzi'
        db.delete_table('hanzi_basics_hanzi')

        # Removing M2M table for field syllables on 'Hanzi'
        db.delete_table('hanzi_basics_hanzi_syllables')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sound': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tone': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hanzi_basics']
