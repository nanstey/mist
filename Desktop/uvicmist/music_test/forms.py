from django import forms
from .models import VoiceRange, Scale, Interval

class VoiceRangeForm(forms.Form):
    voice_range = forms.ModelChoiceField(queryset=VoiceRange.objects.all(), widget=forms.RadioSelect, empty_label=None, label="")
    
class StartForm(forms.Form):
    voicerange = forms.ModelChoiceField(queryset=VoiceRange.objects.all(), widget=forms.RadioSelect, empty_label=None, label="Voice Range:")
    scale = forms.ModelChoiceField(queryset=Scale.objects.all(), widget=forms.RadioSelect, empty_label=None, label="Scale:")
    
class IntervalForm(forms.Form):
    intervals = forms.ModelMultipleChoiceField(queryset=Interval.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class':'intervalCheckbox',}), label="Intervals:",)
    direction = forms.ChoiceField(choices=[(1,'Ascending'),(-1,'Descending'),(0,'Both')], widget=forms.RadioSelect, label="Direction:")
    
class SetupForm(forms.Form):
    voicerange = forms.ModelChoiceField(queryset=VoiceRange.objects.all(), widget=forms.RadioSelect, empty_label=None, label="Voice Range:")
    intervals = forms.ModelMultipleChoiceField(queryset=Interval.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class':'intervalCheckbox',}), label="Intervals:",)
    direction = forms.ChoiceField(choices=[(1,'Ascending'),(-1,'Descending'),(0,'Both')], widget=forms.RadioSelect, label="Direction:")    
    