from rest_framework import serializers
from .models import *


class MentorsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Clients
        fields = ['id', 'user']


class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ("id",'user', "job_position")


class MentorRegistrationSerializer(serializers.ModelSerializer):
    Services = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=True)

    class Meta:
        model = Mentor
        fields = [ 'user','job_position', 'Services', 'banner']

    def create(self, validated_data):
        services = validated_data.pop('Services')
        mentor = Mentor.objects.create(**validated_data)
        mentor.Services.set(services)
        return mentor


class ClientRegistrationSerializer(serializers.ModelSerializer):
    looking_for = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=True)

    class Meta:
        model = Clients
        fields = ['looking_for']

    def create(self, validated_data):
        looking_for = validated_data.pop('looking_for')
        client = Clients.objects.create(**validated_data)
        client.looking_for.set(looking_for)
        return client

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'