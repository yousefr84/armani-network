from rest_framework import serializers
from .models import *


# class MentorsDetailsSerializer(serializers.ModelSerializer):
#   class Meta:
#      model = Mentor
#     fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id",
                  "is_superuser",
                  "username",
                  "is_staff",
                  "email",
                  "phone",
                  "Photo",
                  "last_login",
                  "date_joined",
                  "identification_code",
                  "last_name",
                  "first_name",
                  "is_mentor",
                  "is_active",
                  "groups",
                  "user_permissions",
                  'looking_for')


class MentorsDetailsSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Mentor
        fields = '__all__'


# class CustomUserSerializer(serializers.ModelSerializer):
#     photo_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomUser
#         fields = (
#             "id",
#             "is_superuser",
#             "username",
#             "is_staff",
#             "email",
#             "phone",
#             "Photo",
#             "photo_url",
#             "last_login",
#             "date_joined",
#             "identification_code",
#             "last_name",
#             "first_name",
#             "is_mentor",
#             "is_active",
#             "groups",
#             "user_permissions",
#             "looking_for",
#         )
#
#     def get_photo_url(self, obj):
#         request = self.context.get('request')
#         if obj.Photo and request:
#             return request.build_absolute_uri(obj.Photo.url)
#         return None


class MentorListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Mentor
        fields = ("id", 'user', "job_position")


class MentorRegistrationSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Mentor
        fields = ['user', 'job_position', 'services', 'banner', 'project']

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
