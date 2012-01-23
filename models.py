#coding='utf-8'
from __future__ import print_function, division, unicode_literals
from django.db import models
from hanzi_basics.pinyin_nums_to_markers import pinyin_nums_to_markers

class PinyinSyllable(models.Model):
    sound = models.CharField(max_length=10)
    tone = models.IntegerField()

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
        # Sounds are stored in the database using utf-8, convert to unicode.
        utf8_sound = self.sound
        u_sound = utf8_sound.decode('utf-8')

        return "{0}{1}".format(u_sound, self.tone)

    def marker_display(self):
        numerical = '{0}'.format(self)
        marker = pinyin_nums_to_markers[numerical]
        return marker

class Hanzi(models.Model):
    syllables = models.ManyToManyField(PinyinSyllable)
    char = models.CharField(max_length=1, unique=True)
    # The rank from ordering characters by frequency of use.
    # Most used character is rank 1.
    use_rank = models.IntegerField(null=True, blank=True)

    @staticmethod
    def get_or_create(char, use_rank):
        """ @brief Gets the corresponding Hanzi if it exists, else creates and returns
                it.
        """
        hs = Hanzi.objects.filter(char=char)
        if not hs.exists():
            nh = Hanzi(char=char, use_rank=use_rank)
            nh.save()
            h = nh
        elif hs.count() > 1:
            msg = "More than one hanzi '{0}' (rank {1}).".format(char, use_rank)
        else:
            h = hs[0]
        
        return h

    def __unicode__(self):
	# char is stored in utf8, convert to unicode for use here.
        urep = "({0}) {1} ({2} sounds)"\
                   .format(self.use_rank, self.char, self.syllables.count())
        return urep
