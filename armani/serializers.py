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


class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ("id", 'user', "job_position")


class MentorRegistrationSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Mentor
        fields = ['user', 'job_position', 'services', 'banner']

    def create(self, validated_data):
        services = validated_data.pop('services', None)
        mentor = Mentor.objects.create(**validated_data)
        if services:
            mentor.services.set(services)
        return mentor


class ClientRegistrationSerializer(serializers.ModelSerializer):
    looking_for = serializers.PrimaryKeyRelatedField(
        queryset=Services.objects.all(), many=True, required=False
    )

    class Meta:
        model = CustomUser
        fields = ['looking_for']

    def create(self, validated_data):
        looking_for = validated_data.pop('looking_for', None)
        client = CustomUser.objects.create(**validated_data)
        if looking_for:
            client.looking_for.set(looking_for)
        return client


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image', 'is_finished']


class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['name', 'public_by', 'img', 'is_readed']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
