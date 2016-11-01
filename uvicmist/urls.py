"""interval_singing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from music_test import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    # url(r'^voicerange/', views.get_voice_range, name='voicerange'),
    # url(r'^vrapi/(?P<vr_id>\d+)/$', views.VoiceRangeDetails.as_view() ),
    url(r'^vr/(?P<pk>\d+)/$', views.VoiceRangeDetails.as_view() ),
    # url(r'^all_voiceranges/', views.all_voiceranges, name='all_voiceranges'),
    # url(r'^voicerange_details/(?P<vr_id>\d+)/$', views.voicerange_details, name='voicerange_details')
    url(r'^setup/', views.setup, name='setup'),
    # url(r'^scale/', views.get_voicerange_scale, name='scale'),
    # url(r'^intervals/', views.intervals, name='intervals'),
    url(r'^test/', views.test, name='name'),
    # url(r'^recorder/', TemplateView.as_view(template_name='example_simple_exportwav.html'), name='recorder')
    url(r'^submit.', views.submit, name='submit'),
    url(r'^exit/', views.exit, name='exit'),
]

urlpatterns = format_suffix_patterns(urlpatterns)