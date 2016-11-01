from __future__ import unicode_literals
from music21 import *
from django.db import models
from random import random, randrange

# Create your models here.
class VoiceRange(models.Model):
    vr_name = models.CharField(max_length=32, verbose_name = 'Voice Range Name')  # Voice Range Name
    vr_bot = models.CharField(max_length=3, verbose_name = 'Voice Range Bottom')  # Voice Range Bottom, music21 note names ( C4, F#3, E-5)
    vr_top = models.CharField(max_length=3, verbose_name = 'Voice Range Top')     # Voice Range Top, music21 note names ( C4, F#3, E-5)

    class Meta:
        ordering = ['pk']
        
    def create(self, vr_name, vr_bot, vr_top):
        self.vr_name = vr_name
        self.vr_bot = vr_bot
        self.vr_top = vr_top

    def __str__(self):
        return self.vr_name
    
    def bot(self):
        return self.vr_bot
    
    def top(self):
        return self.vr_top

    # def printRange(self):
    #     bot = note.Note(self.vr_bot)
    #     top = note.Note(self.vr_top)      
    #     bot.duration.type = 'whole'
    #     top.duration.type = 'whole'      
    #     rangeStream = stream.Stream()
    #     rangeStream.append(bot)
    #     rangeStream.append(top)
    #     rangeStream.clef = clef.BassClef()
    #     rangeStream.write('lily.png')
        
class Scale(models.Model):
    sc_name = models.CharField(max_length=32, verbose_name = 'Scale Name')  # Scale Name
    sc_root = models.CharField(max_length=2, verbose_name = 'Scale Root')   # Scale root, music21 note names
    sc_type = models.BooleanField(verbose_name = 'Diatonic (Major)') # 1 for Major, 0 for Chromatic
    
    class Meta:
        ordering = ['sc_type', 'sc_root']
        
    def create(self, sc_name, sc_root, sc_type):
        self.sc_name = sc_name
        self.sc_root = sc_root
        self.sc_type = sc_type
    
    def __str__(self):
        return self.sc_name
    
    def root(self):
        return self.sc_root
    
    def type(self):
        return self.sc_type

class Interval(models.Model):
    iv_name = models.CharField(max_length=32, verbose_name = 'Interval Name')
    iv_abrv = models.CharField(max_length=2, verbose_name = 'Interval Abbreviation')
    iv_dist = models.IntegerField(verbose_name = 'Interval Distance (Semitones)')
    
    class Meta:
        ordering = ['iv_dist']
        
    def __str__(self):
        return self.iv_name
    
    def abrv(self):
        return self.iv_abrv
    
    def dist(self):
        return self.iv_dist
 
class IntervalManager(models.Model):
    interval_list = [ [] for x in xrange(13) ]
    active_intervals = []
    num_intervals = 0
    active_direction = 0
    attempts = 0
    correct = 0
    tested_intervals = []
    current_notes = {}
    current_interval = []
    current_direction = []
    
   
    def __init__(self,VoiceRange, Intervals, Direction):
        # Initialize variables
        self.interval_list = [ [] for x in xrange(13) ]
        self.active_intervals = []
        self.num_intervals = 0
        self.active_direction = 0
        self.attempts = 0
        self.correct = 0
        self.tested_intervals = []
        # Call helper functions to set variables
        self.make_list(VoiceRange)
        self.set_active(Intervals, Direction)
        
        
 
    # def set_list(self, Voicerange):
    #     temp_scale = scale.ChromaticScale( 'C' ) # scale.ChromaticScale from music21
    #     pitches = [ str(p) for p in temp_scale.getPitches( VoiceRange.bot(), VoiceRange.top() ) ] # Generates list of pitches from a scale within a range
    #     # Populate list
    #     length = len(pitches)
    #     for i in range (self.num_intervals): # i = index of interval
    #         j = self.interval_list[i][0] # j = interval distance in semitones
    #         
    
    def make_list(self, VoiceRange):
        temp_scale = scale.ChromaticScale( 'C' ) # scale.ChromaticScale from music21
        pitches = [ str(p) for p in temp_scale.getPitches( VoiceRange.bot(), VoiceRange.top() ) ] # Generates list of pitches from a scale within a range
        # For loop to populate intervals_list
        length = len(pitches)
        for x in range(length):
            for y in range(x,length):
                note1 = pitch.Pitch( pitches[x] )   # x is the first list pointer location
                note2 = pitch.Pitch( pitches[y] )   # y is the second list pointer location            
                z = note2.midi - note1.midi         # z is the interval in semitones
                if ( z > 12 ) :
                    break
                self.interval_list[z].append( ( pitches[x],pitches[y] ) )   # insert interval as note tuple into interval_list 
    
    def set_active(self, Intervals, Direction):
        self.active_direction = Direction
        active_intervals = []
        for Interval in Intervals:
            active_intervals.append( [int(Interval.dist()), str(Interval.abrv()), str(Interval)] )
        self.active_intervals = active_intervals
        self.num_intervals = len(active_intervals)
        
    def next(self):
        x = randrange(0, self.num_intervals) # x = index for testable intervals
        y = self.active_intervals[x][0] # y = interval in semitones
        listlen = len( self.interval_list[y] ) # listlen for that interval
        z = randrange(0, listlen) # z = random index for that list
        interval_tuple = self.interval_list[y][z] # selected tuple
        
        # Check direction
        direction = 1
        if int(self.active_direction) > 0:
            # Keep ascending order
            interval_tuple = interval_tuple
        if int(self.active_direction) < 0:
            # Flip to descending order
            interval_tuple = self.reverse(interval_tuple)
            direction = -1
        elif int(self.active_direction) == 0:
            # Flip half the time
            if round( random() ):
                interval_tuple = self.reverse(interval_tuple)
                direction = -1
        self.current_notes = interval_tuple
        self.current_interval = self.active_intervals[x]
        self.current_direction = direction
        # print(self.current_notes[0])
        # print(self.current_notes[1])
        # print(self.active_intervals)
        return [interval_tuple, self.active_intervals[x], direction]
    
    def reverse(self, interval_tuple):
        interval_tuple = reversed(interval_tuple)
        return tuple(interval_tuple)
               
    def list(self):
        return self.interval_list
    
    def intervals(self):
        return self.active_intervals
    
    def direction(self):
        return self.active_direction   
    
    def checkNotes(self, firstNote, secondNote):
        
        if ((firstNote == self.current_notes[0]) and (secondNote == self.current_notes[1])):
            self.attempts += 1
            self.correct += 1
            self.tested_intervals.append( [self.current_interval[2], self.current_direction, True] )
            print self.attempts
            print self.correct
            print self.tested_intervals
            return 1
        else:
            self.attempts += 1
            self.tested_intervals.append( [self.current_interval[2], self.current_direction, False] )
            print self.attempts
            print self.correct
            print self.tested_intervals
            return 0
        
    def score(self):
        return str(self.correct) + "/" + str(self.attempts)
    
    def history(self):
        return self.tested_intervals
    
    def printNice(self):
        print "Interval List:"
        for x in xrange(13):
            # print('\n{} - Number of intervals = {}' .format(x, len(self.interval_list[x])) )
            print self.interval_list[x]
        print "Active Intervals:"
        print self.active_intervals
        print "Direction:"
        print self.active_direction
