from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class MainListAPIView(APIView):
    def get(self, request):
        mentors = Mentor.objects.all()
        mentor_serializer = MentorListSerializer(mentors, many=True)
        mentor_data = [{"type": "Mentor", **data} for data in mentor_serializer.data]

        projects = Project.objects.all()
        project_serializer = ProjectListSerializer(projects, many=True)
        project_data = [{"type": "Project", **data} for data in project_serializer.data]

        article = Articles.objects.all()
        article_serializer = ArticleListSerializer(article, many=True)
        article_data = [{"type": "Article", **data} for data in article_serializer.data]

        combined_data = mentor_data + project_data + article_data

        return Response(combined_data, status=status.HTTP_200_OK)


class MentorListAPIView(APIView):
    def get(self, request):
        mentors = Mentor.objects.all()
        mentor_serializer = MentorListSerializer(mentors, many=True)
        return Response(mentor_serializer.data, status=status.HTTP_200_OK)


class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        project_serializer = ProjectListSerializer(projects, many=True)
        return Response(project_serializer.data, status=status.HTTP_200_OK)


class ArticleListAPIView(APIView):
    def get(self, request):
        articles = Articles.objects.all()
        article_serializer = ArticleListSerializer(articles, many=True)
        return Response(article_serializer.data, status=status.HTTP_200_OK)


class ServicesListAPIView(APIView):
    def get(self, request):
        services = Services.objects.all()
        services_serializer = ServiceSerializer(services, many=True)
        services_data = services_serializer.data
        return Response(services_data, status=status.HTTP_200_OK)


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
        try:
            mentor = Mentor.objects.get(user=request.user)
        except Mentor.DoesNotExist:
            return Response({"error": "Mentor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MentorsDetailsSerializer(mentor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        permission_classes([IsAuthenticated])
        try:
            mentor = Mentor.objects.get(user=request.user)
        except Mentor.DoesNotExist:
            return Response({"error": "Mentor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if mentor.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to delete this account."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = mentor.user
        mentor.delete()
        user.delete()

        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)


class ProjectDetailAPIView(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, id=id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        permission_classes([IsAuthenticated])
        id = request.query_params.get('id', None)
        if id is None:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, id=id)

        if project.manager != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to update this project."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectDetailSerializer(project, data=request.data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, id=id)

        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can delete projects."},
                status=status.HTTP_403_FORBIDDEN
            )

        project.delete()

        return Response({"message": "Project deleted successfully."}, status=status.HTTP_200_OK)


class ArticleDetailAPIView(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        article = get_object_or_404(Articles, id=id)
        serializer = ArticleDetailsSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        permission_classes([IsAuthenticated])
        id = request.query_params.get('id', None)
        if id is None:
            return Response({"error": "Article ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        article = get_object_or_404(Articles, id=id)

        if article.public_by != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to update this article."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleDetailsSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response({"error": "Article ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        article = get_object_or_404(Articles, id=id)

        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can delete articles."},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()

        return Response({"message": "Article deleted successfully."}, status=status.HTTP_200_OK)


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
