# coding='utf-8'
from __future__ import print_function, division, unicode_literals

from django.db import models
from hanzi_basics.pinyin_nums_to_markers import num_to_tone
import logging
import encodings

logger = logging.getLogger(__name__)

class PinyinSyllable(models.Model):
    sound = models.CharField(max_length=10)
    tone = models.IntegerField()
    display = models.CharField(max_length=10)

    # --- 2016-03-19 These might still be used by another package.
    #    Leaving them here, unused, so I don't have to worry about breaking
    #    something.
    verified = models.BooleanField(default=False)
    # If an unverified syllable is added, the context id should point to the
    #    context which caused the syllable to be added.
    context_id = models.IntegerField(null=True, blank=True)

#     def __unicode__(self):
#         return "{0}{1} ({2})".format(self.sound, self.tone, self.display)

    # 2016-03-19 Probably before built-in or just didn't know there was a built-in.
    #    Remove if here past 2016-05-01
#     @staticmethod
#     def get_or_create(sound, tone):
#         """ @brief If the syllable with 'sound' and 'tone' doesn't exist, create it.
#                 Return the syllable regardless.
#         """
#         # Pinyin Syllables
#         pss = PinyinSyllable.objects.filter(sound=sound, tone=tone)
#
#         if not pss.exists():
#             # New pinyin syllable
#             nps = PinyinSyllable(sound=sound, tone=tone)
#             nps.save()
#             ps = nps
#         elif pss.count() > 1:
#             msg = "There are {0} syllables '{1}{2}'".format(pss.count(), sound, tone)\
#                       .encode('utf8')
#             raise Exception(msg)
#         else:
#             ps = pss[0]
#
#         return ps

    def marker_display(self):
        numerical = '{0}{1}'.format(self.sound, self.tone)
        marker = num_to_tone(numerical)
        return marker

class Hanzi(models.Model):
    syllables = models.ManyToManyField(PinyinSyllable)
    char = models.CharField(max_length=10, unique=True)
    # The number of times this character was used in the sample
    #    (See script in populate_models for details).
    use_count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        u = self.char.decode('utf-8')
        return u

    # --- 2016-03-19 These might still be used by another package.
#     verified = models.BooleanField(default=False)
#     # If an unverified hanzi is added, the context id should point to the
#     #    context which caused the hanzi to be added.
#     context_id = models.IntegerField(null=True, blank=True)
#
#     @staticmethod
#     def get_or_create(char, pinyin=None, use_rank=None):
#         """ @brief Gets the corresponding Hanzi if it exists, else creates and returns
#                 it.
#             @param pinyin is an iterable of PinyinSyllable instances representing
#                 the pronunciations for \a char.  If \a char doesn't exist,
#                 \a pinyin must be an iterable with at least one PinyinSyllable.
#             @param use_rank if known, is the ranking for how frequently the
#                 character is used in mandarin.
#         """
#         hs = Hanzi.objects.filter(char=char)
#         if not hs.exists():
#             # Ensure pinyin has been included
#             if pinyin is None or len(pinyin) < 1:
#                 msg = "Parameter 'pinyin' must be set for new Hanzi instance '{}'"\
#                           .format(char)
#                 logger.error(msg)
#                 raise Exception(msg)
#
#             nh = Hanzi(char=char, use_rank=use_rank)
#             nh.save()
#             # linked syllables
#             nh.syllables.add(*pinyin)
#
#             h = nh
#         elif hs.count() > 1:
#             msg = "More than one hanzi '{0}' (rank {1}).".format(char, use_rank)
#             logger.warning(msg)
#             h = hs[0]
#         else:
#             h = hs[0]
#
#         return h
