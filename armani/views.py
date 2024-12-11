from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class MentorsListAPIView(APIView):
    def get(self, request):
        mentors = Mentor.objects.all()
        mentor_serializer = MentorListSerializer(mentors, many=True)
        mentor_data = [{"type": "mentor", **data} for data in mentor_serializer.data]

        projects = Project.objects.all()
        project_serializer = ProjectListSerializer(projects, many=True)
        project_data = [{"type": "project", **data} for data in project_serializer.data]

        combined_data = mentor_data + project_data

        return Response(combined_data, status=status.HTTP_200_OK)


class MentorsDetailAPIView(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        mentor = get_object_or_404(Mentor, id=id)
        serializer = MentorsDetailsSerializer(mentor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        permission_classes([IsAuthenticated])
        id = request.data.get('id', None)
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        mentor = get_object_or_404(Mentor, id=id)
        serializer = MentorsDetailsSerializer(mentor, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        is_mentor = user_data.get('is_mentor', False)

        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()
            if is_mentor:
                mentor_data = {
                    "user": user.id,
                    "phone": user_data.get("phone"),
                    "job_position": user_data.get("job_position"),
                    "Services": user_data.get("Services", []),
                    "banner": user_data.get("banner")
                }
                mentor_serializer = MentorRegistrationSerializer(data=mentor_data)
                if mentor_serializer.is_valid():
                    mentor_serializer.save(user=user)
                else:
                    user.delete()
                    return Response(mentor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                client_data = {
                    "user": user.id,
                    "looking_for": user_data.get("looking_for", [])
                }
                client_serializer = ClientRegistrationSerializer(data=client_data)
                if client_serializer.is_valid():
                    client_serializer.save(user=user)
                else:
                    user.delete()
                    return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


