from rest_framework import serializers
from .models import *


# class MentorsDetailsSerializer(serializers.ModelSerializer):
#   class Meta:
#      model = Mentor
#     fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    manager = serializers.StringRelatedField()  # نمایش نام مدیر پروژه

    class Meta:
        model = Project
        fields = ['name', 'description', 'photo', 'is_finished', 'manager', 'photo_url']

    def get_photo_url(self, obj):
        # تغییر: تولید URL کامل برای عکس پروژه
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()  # اضافه کردن فیلد جدید
    projects = serializers.SerializerMethodField()
    services = serializers.SlugRelatedField(
        many=True,  # چون ManyToManyField است
        read_only=True,  # یا اگر می‌خواهی قابلیت تغییر داشته باشد، این خط را حذف کن
        slug_field="name"  # نام فیلدی که برای نمایش یا ذخیره از آن استفاده می‌شود
    )
    looking_for = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = CustomUser
        fields = ("id",

                  "is_superuser",
                  "username",
                  "is_staff",
                  "email",
                  "phone",
                  "Photo",
                  "photo_url",
                  "last_login",
                  "date_joined",
                  "identification_code",
                  "last_name",
                  "first_name",
                  'services',
                  'banner',
                  'project',
                  'city',
                  'social_networks',
                  'country',
                  'resume',
                  'company',
                  "is_active",
                  "groups",
                  "user_permissions",
                  "looking_for",
                  'job_position',
                  'projects')
        extra_kwargs = {
            'project': {'required': False},
            'services': {'required': False},
        }

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.Photo and request:
            return request.build_absolute_uri(obj.Photo.url)
        return None

    def get_projects(self, obj):
        projects = obj.projects_members.all()  # استفاده از related_name='projects_members'
        request = self.context.get('request')
        return ProjectListSerializer(projects, many=True, context={'request': request}).data


# class ProjectListSerializer(serializers.ModelSerializer):
#     photo_url = serializers.SerializerMethodField()
#     manager = CustomUserSerializer()
#
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'photo', 'is_finished', 'manager', 'photo_url']
#
#     def get_photo_url(self, obj):
#         request = self.context.get('request')
#         if obj.photo and request:
#             return request.build_absolute_uri(obj.photo.url)
#         return None


# class MentorsDetailsSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#
#     class Meta:
#         model = Mentor
#         fields = '__all__'


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

class UserListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", 'user', "job_position", "photo_url")

    def get_photo_url(self, obj):
        # دسترسی به عکس کاربر
        request = self.context.get('request')
        if obj.user.Photo and request:
            return request.build_absolute_uri(obj.Photo.url)
        return None


# class MentorListSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#     photo_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Mentor
#         fields = ("id", 'user', "job_position", "photo_url")
#
#     def get_photo_url(self, obj):
#         # دسترسی به عکس کاربر
#         request = self.context.get('request')
#         if obj.user.Photo and request:
#             return request.build_absolute_uri(obj.user.Photo.url)
#         return None


# class MentorRegistrationSerializer(serializers.ModelSerializer):
#     banner = serializers.ImageField(required=False, allow_null=True)
#
#     class Meta:
#         model = Mentor
#         fields = ['user', 'job_position', 'services', 'banner', 'project']
#
#     def create(self, validated_data):
#         services = validated_data.pop('services', None)
#         mentor = Mentor.objects.create(**validated_data)
#         if services:
#             mentor.services.set(services)
#         return mentor


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


class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    public_by = CustomUserSerializer()

    class Meta:
        model = Articles
        fields = ['name', 'public_by', 'type', 'photo', 'is_readed', 'photo_url']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None



