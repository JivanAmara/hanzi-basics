#coding='utf-8'
from __future__ import print_function, division, unicode_literals

from django.db import models
from hanzi_basics.pinyin_nums_to_markers import num_to_tone
import logging

logger = logging.getLogger(__name__)

class PinyinSyllable(models.Model):
    sound = models.CharField(max_length=10)
    tone = models.IntegerField()
    display = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)
    # If an unverified syllable is added, the context id should point to the
    #    context which caused the syllable to be added.
    context_id = models.IntegerField(null=True, blank=True)
    
    @staticmethod
    def get_or_create(sound, tone):
        """ @brief If the syllable with 'sound' and 'tone' doesn't exist, create it.
                Return the syllable regardless.
        """
        # Pinyin Syllables
        pss = PinyinSyllable.objects.filter(sound=sound, tone=tone)

        if not pss.exists():
            # New pinyin syllable
            nps = PinyinSyllable(sound=sound, tone=tone)
            nps.save()
            ps = nps
        elif pss.count() > 1:
            msg = "There are {0} syllables '{1}{2}'".format(pss.count(), sound, tone)\
                      .encode('utf8')
            raise Exception(msg)
        else:
            ps = pss[0]
        
        return ps

    def __unicode__(self):
        return "{0}{1} ({2})".format(self.sound, self.tone, self.display)

    def marker_display(self):
        numerical = '{0}{1}'.format(self.sound, self.tone)
        marker = num_to_tone(numerical)
        return marker

class Hanzi(models.Model):
    syllables = models.ManyToManyField(PinyinSyllable)
    char = models.CharField(max_length=1, unique=True)
    # The rank from ordering characters by frequency of use.
    # Most used character is rank 1.
    use_rank = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    # If an unverified hanzi is added, the context id should point to the
    #    context which caused the hanzi to be added.
    context_id = models.IntegerField(null=True, blank=True)

    @staticmethod
    def get_or_create(char, pinyin=None, use_rank=None):
        """ @brief Gets the corresponding Hanzi if it exists, else creates and returns
                it.
            @param pinyin is an iterable of PinyinSyllable instances representing
                the pronunciations for \a char.  If \a char doesn't exist,
                \a pinyin must be an iterable with at least one PinyinSyllable.
            @param use_rank if known, is the ranking for how frequently the 
                character is used in mandarin.
        """
        hs = Hanzi.objects.filter(char=char)
        if not hs.exists():
            # Ensure pinyin has been included
            if pinyin is None or len(pinyin) < 1:
                msg = "Parameter 'pinyin' must be set for new Hanzi instance '{}'"\
                          .format(char)
                logger.error(msg)
                raise Exception(msg)

            nh = Hanzi(char=char, use_rank=use_rank)
            nh.save()
            # linked syllables
            nh.syllables.add(*pinyin)
            
            h = nh
        elif hs.count() > 1:
            msg = "More than one hanzi '{0}' (rank {1}).".format(char, use_rank)
            logger.warning(msg)
            h = hs[0]
        else:
            h = hs[0]
        
        return h

    def __unicode__(self):
        # char is stored in utf8, convert to unicode for use here.
        urep = "({0}) {1} ({2} sounds)"\
                   .format(self.use_rank, self.char, self.syllables.count())
        return urep
