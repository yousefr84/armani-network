from rest_framework import serializers
from .models import *

class MentorsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentors
        fields = '__all__'

class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentors
        fields = ("id","name","job_position")