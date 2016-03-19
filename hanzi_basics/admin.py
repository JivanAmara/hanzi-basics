# coding=utf-8
""" @brief
    @author jivan
    @updated Aug 20, 2011
"""
from __future__ import unicode_literals, print_function, division
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from hanzi_basics.models import Hanzi, PinyinSyllable

class PinyinSyllableAdmin(ModelAdmin):
    list_filter = ('sound', 'tone')

class HanziAdmin(ModelAdmin):
    ordering = ('-use_count',)

admin.site.register(Hanzi, HanziAdmin)
admin.site.register(PinyinSyllable, PinyinSyllableAdmin)
