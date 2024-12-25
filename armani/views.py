from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class MainListAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        users_serializer = CustomUserSerializer(users, many=True, context={"request": request})
        # users_data = users_serializer.data

        projects = Project.objects.all()
        project_serializer = ProjectListSerializer(projects, many=True, context={"request": request})
        # project_data = [{"type": "Project", **data} for data in project_serializer.data]

        article = Articles.objects.all()
        article_serializer = ArticleListSerializer(article, many=True, context={"request": request})
        # article_data = [{"type": "Article", **data} for data in article_serializer.data]

        # combined_data = mentor_data + project_data + article_data
        combined = {
            "users": users_serializer.data,
            "projects": project_serializer.data,
            "articles": article_serializer.data,
        }
        return Response(combined, status=status.HTTP_200_OK)


# class MentorListAPIView(APIView):
#     permission_classes([IsAuthenticated])
#
#     def get(self, request):
#         mentors = Mentor.objects.all()
#         mentor_serializer = MentorListSerializer(mentors, many=True)
#         return Response(mentor_serializer.data, status=status.HTTP_200_OK)
#
#
# class ProjectListAPIView(APIView):
#     def get(self, request):
#         projects = Project.objects.all()
#         project_serializer = ProjectListSerializer(projects, many=True)
#         return Response(project_serializer.data, status=status.HTTP_200_OK)
#
#
# class ArticleListAPIView(APIView):
#     def get(self, request):
#         articles = Articles.objects.all()
#         article_serializer = ArticleListSerializer(articles, many=True)
#         return Response(article_serializer.data, status=status.HTTP_200_OK)
class CustomUserList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = CustomUser.objects.all()
        users_serializer = CustomUserSerializer(users, many=True, context={"request": request})
        return Response(users_serializer.data, status=status.HTTP_200_OK)


class ServicesListAPIView(APIView):
    def get(self, request):
        services = Services.objects.all()
        services_serializer = ServiceSerializer(services, many=True)
        services_data = services_serializer.data
        return Response(services_data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('id', None)
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_id = request.data.get('id', None)
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True, context={"request": request})
        print(f"serialized user data : {serializer.is_valid()}")
        print(f"user data is:   {serializer.data}")

        if serializer.is_valid():
            serializer.save()
            print(f"user data is:   {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(f"serializer error is :   {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user_id = request.data.get('id', None)  # گرفتن شناسه کاربر
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)  # یافتن کاربر
        serializer = CustomUserSerializer(user, data=request.data, partial=True, context={"request": request})
        print(f"validations of serializer is : {serializer.is_valid()}")
        print(f"user data is:   {serializer.data}")
        if serializer.is_valid():
            serializer.save()
            print(f"user data is:   {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(f"serializer error is :   {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#
#         try:
#             mentor = Mentor.objects.get(user=user)
#         except Mentor.DoesNotExist:
#             mentor = None
#
#         user_serializer = CustomUserSerializer(user, context={"request": request})
#         mentor_serializer = MentorsDetailsSerializer(mentor, context={"request": request}) if mentor else None
#
#         response_data = {
#             "user": user_serializer.data,
#             "mentor": mentor_serializer.data if mentor_serializer else None,
#         }
#
#         return Response(response_data, status=status.HTTP_200_OK)


# class MentorsDetailAPIView(APIView):
#     def post(self, request):
#         id = request.data.get('id', None)
#         if not id:
#             return Response({"error": "MentorID is required."}, status=status.HTTP_400_BAD_REQUEST)
#         mentor = get_object_or_404(Mentor, id=id)
#         mentor_serializer = MentorsDetailsSerializer(mentor)
#         return Response(mentor_serializer.data, status=status.HTTP_200_OK)
#
#     # def get(self, request):
#     #     id = request.query_params.get('id', None)
#     #     if id is None:
#     #         return Response(status=status.HTTP_400_BAD_REQUEST)
#     #     mentor = get_object_or_404(Mentor, id=id)
#     #     serializer = MentorsDetailsSerializer(mentor)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request):
#         permission_classes([IsAuthenticated])
#         try:
#             mentor = Mentor.objects.get(user=request.user)
#         except Mentor.DoesNotExist:
#             return Response({"error": "Mentor profile not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = MentorsDetailsSerializer(mentor, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         permission_classes([IsAuthenticated])
#         try:
#             mentor = Mentor.objects.get(user=request.user)
#         except Mentor.DoesNotExist:
#             return Response({"error": "Mentor profile not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         if mentor.user != request.user and not request.user.is_staff:
#             return Response(
#                 {"error": "You do not have permission to delete this account."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#
#         user = mentor.user
#         mentor.delete()
#         user.delete()
#
#         return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)


class ProjectDetailAPIView(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, id=id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(manager=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        serializer = ArticleDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()

            return Response(CustomUserSerializer(user, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
