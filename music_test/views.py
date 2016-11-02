from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from .models import VoiceRange, IntervalManager
from .forms import VoiceRangeForm, StartForm, IntervalForm, SetupForm
from rest_framework import generics
from serializers import VoiceRangeSerializer
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

class VoiceRangeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = VoiceRange.objects.all()
    serializer_class = VoiceRangeSerializer
    
# def get_voicerange_scale(request):
#     if request.method =='POST':
#         form = StartForm(request.POST)
#         if form.is_valid():
#             request.session['voicerange'] = form.cleaned_data['voicerange']
#             request.session['scale'] = form.cleaned_data['scale']
#             return HttpResponseRedirect('/intervals/')
#     else:
#         form = StartForm()
#     return render(request, 'scale.html', {'form': form})
# 
# def intervals(request):
#     if request.method == 'POST':
#         form = IntervalForm(request.POST)
#         if form.is_valid():
#             request.session['intervals'] = form.cleaned_data['intervals']
#             request.session['direction'] = form.cleaned_data['direction']
#             return HttpResponseRedirect('/test/')
#     else:
#         form = IntervalForm()
#     return render(request, 'intervals.html', {'form': form})

def setup(request):
    if request.method == 'POST':
        form = SetupForm(request.POST)
        if form.is_valid():
            request.session['voicerange'] = form.cleaned_data['voicerange']
            request.session['intervals'] = form.cleaned_data['intervals']
            request.session['direction'] = form.cleaned_data['direction']
            return HttpResponseRedirect('/test/')
    else:
        form = SetupForm()
    return render(request, 'setup.html', {'form': form})

def test(request):
    if(request.GET.get('next')):
        # try:
        Manager = request.session['Manager']
        next_interval = Manager.next()
        score = Manager.score()
        request.session['Manager'] = Manager
        # print("Next Interval: {}" .format(next_interval) )
        context2 = {}
        context2['first_note'] = next_interval[0][0].replace('#','+')
        context2['second_note'] = next_interval[0][1].replace('#','+')
        context2['interval_name'] = next_interval[1][2]
        context2['direction'] = next_interval[2]
        context2['score'] = score
        return render(request, 'test_interval.html', context2)
        # except UnboundLocalError:
        #     print("There was a problem...")
    else:    
        # Get session info
        VoiceRange = request.session['voicerange']
        Intervals = request.session['intervals']
        Direction = request.session['direction']
        # Create IntervalManager
        Manager = IntervalManager(VoiceRange, Intervals, Direction)
        request.session['Manager'] = Manager
        # Manager.printNice()
        # Set Context
        context = {}
        context['list'] = Manager.list()
        context['intervals'] = Manager.intervals()
        context['direction'] = Manager.direction()
        context['msg'] = "Ready? Press 'Next Interval' to begin"
        # Render template
        return render(request, 'test_frame.html', context)
    
def submit(request):
    notes = json.loads(request.body)
    if len(notes) > 2:
        return HttpResponse('{ "message" : "<span style=\'color:red\'>Too many notes detected.</span> Please try again.", "playnote" : "False" }', content_type="application/json")
    if len(notes) < 2:
        return HttpResponse('{ "message" : "<span style=\'color:red\'>Too few notes detected.</span> Please try again.", "playnote" : "False" }', content_type="application/json")
    
    Manager = request.session['Manager']
    isCorrect = Manager.checkNotes(notes[0]["pitch"], notes[1]["pitch"])
    request.session['Manager'] = Manager
    
    if isCorrect:
        return HttpResponse('{ "message" : "<span style=\'color:green\'>Correct!</span> Continue to next interval.", "playnote" : "False" }', content_type="application/json")
    return HttpResponse('{ "message" : "<span style=\'color:red\'>Incorrect!</span> Try again or continue to next interval.", "playnote" : "True" }', content_type="application/json")

def exit(request):
    Manager = request.session['Manager']
    context = {}
    context['score'] = Manager.score()
    context['tested_intervals'] = Manager.history()
    return render(request, 'exit.html', context)
        

# def get_voice_range(request):
#     if request.method =='POST':
#         form = VoiceRangeForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/home/')    
#     else:
#         form = VoiceRangeForm()
#     return render(request, 'voicerange/voicerange.html', {'form': form})

# def all_voiceranges(request):
#     voiceranges = VoiceRange.objects.all()
#     return render(request, 'voicerange/all_voiceranges.html', {'voiceranges':voiceranges})
# 
# def voicerange_details(request, vr_id):
#     voicerange = VoiceRange.objects.get(pk=vr_id)
#     return render(request, 'voicerange/voicerange_details.html', {'voicerange':voicerange})
