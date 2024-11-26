from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


@api_view(['GET'])
class MentorsListAPIView(APIView):
    def get(self, request):
        mentors = Mentors.objects.all()
        mentor_serializer = MentorListSerializer(mentors, many=True)
        return Response(mentor_serializer.data, status=status.HTTP_200_OK)


class MentorsDetailAPIView(APIView):
    def get(self, request, id):
        mentor = Mentors.objects.get(id=id)
        serializer = MentorsDetailsSerializer(mentor)
        return Response(serializer.data, status=status.HTTP_200_OK)
