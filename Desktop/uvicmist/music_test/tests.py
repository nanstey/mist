from django.test import TestCase
from music_test.models import VoiceRange, Scale, IntervalManager

# Create your tests here.
class VoiceRangeTest(TestCase):
    def setUp(self):
        VoiceRange.objects.create(vr_name="Bass", vr_bot="G2", vr_top="B3")
    
    def test_bass_range_print(self):
        bass = VoiceRange.objects.get(pk=1)
        bass.printRange()

class ScaleTest(TestCase):
    def setUp(self):
        Scale.objects.create(sc_name="C Maj", sc_root="C", sc_type=1)
        
class IntervalListTest(TestCase):
    def test_intervals(self):
        bass = VoiceRange.create("Bass", "G2", "B3")
        cMaj = Scale("C Maj", "C", 1)
        intervals = IntervalManager.create(bass, cMaj)
        print "\n C Maj"
        intervals.printNice()
        
        chrom = Scale("Chromatic", "C", 0)
        intervals = IntervalManager.create(bass, chrom)
        print "\n Chromatic"
        intervals.printNice()