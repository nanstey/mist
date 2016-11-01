from django.contrib import admin
from .models import VoiceRange, Scale, Interval

admin.site.site_header = 'Music Interval Singing Test (MIST) Administration'
admin.site.site_title = 'MIST Admin'

# Register your models here.
class VoiceRangeAdmin(admin.ModelAdmin):
    list_display = ('vr_name', 'vr_bot', 'vr_top')
    list_filter = ['vr_name']

admin.site.register(VoiceRange, VoiceRangeAdmin)

class ScaleAdmin(admin.ModelAdmin):
    list_display = ('sc_name', 'sc_root', 'sc_type')
    list_filter = ['sc_name']
    
admin.site.register(Scale, ScaleAdmin)

class IntervalAdmin(admin.ModelAdmin):
    list_display = ('iv_name', 'iv_abrv', 'iv_dist')
    list_filter = ['iv_name']
    
admin.site.register(Interval, IntervalAdmin) 