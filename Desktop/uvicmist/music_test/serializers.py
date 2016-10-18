from rest_framework import serializers
from models import VoiceRange

class VoiceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceRange