from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, ValidationError



from .models import (
    Profile, Counselor, Test, Appointment, TestResult,
    BlogPost, Feedback, Post
)
from .serializers import (
    UserSerializer, ProfileSerializer, CounselorSerializer, TestSerializer,
    AppointmentSerializer, TestResultSerializer, BlogPostSerializer,
    FeedbackSerializer, CounselorAppointmentSerializer, CounselorProfileSerializer,
    PostSerializer, ClientProfileSerializer
)


# Register
class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user)

        return Response({"message": "User created"})


# Login
class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data})
    


# Counselors
class CounselorListAPI(generics.ListAPIView):
    queryset = Counselor.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CounselorSerializer


class CounselorDetailAPI(generics.RetrieveAPIView):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer


# Tests
class TestListAPI(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


# Blog
class BlogListAPI(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogDetailAPI(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


# Appointment
class AppointmentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)

    def perform_create(self, serializer):

        counselor_id = self.request.data.get("counselor")
        if not counselor_id:
            raise ValidationError({"counselor": "counselor is required."})

        counselor = Counselor.objects.get(id=counselor_id)

        start = serializer.validated_data["start_time"]
        end = start + timedelta(minutes=30)

        serializer.save(
            client=self.request.user,
            counselor=counselor,
            end_time=end
        )

# Test Result
class TestResultAPI(generics.CreateAPIView):
    serializer_class = TestResultSerializer


# Feedback
class FeedbackAPI(generics.CreateAPIView):
    serializer_class = FeedbackSerializer

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
def perform_create(self, serializer):
    start = serializer.validated_data["start_time"]
    end = start + timedelta(minutes=30)
    serializer.save(client=self.request.user, end_time=end)

class CounselorProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.profile.role != "counselor":
            return Response({"detail": "Not counselor"}, status=403)

        serializer = CounselorProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        if request.user.profile.role != "counselor":
            return Response({"detail": "Not counselor"}, status=403)

        serializer = CounselorProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CounselorAppointmentsAPI(generics.ListAPIView):
    serializer_class = CounselorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.profile.role != "counselor":
            return Appointment.objects.none()

        return Appointment.objects.filter(counselor=self.request.user.counselor)

class CounselorAppointmentMarkDoneAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = request.user
        if not hasattr(user, "profile") or user.profile.role != "counselor":
            return Response({"detail": "شما مشاور نیستید."}, status=403)
        try:
            counselor = Counselor.objects.get(user=user)
        except Counselor.DoesNotExist:
            return Response({"detail": "پروفایل مشاور یافت نشد."}, status=404)
        try:
            appointment = Appointment.objects.get(id=pk, counselor=counselor)
        except Appointment.DoesNotExist:
            return Response({"detail": "نوبت یافت نشد."}, status=404)
        appointment.status = "done"
        appointment.save()
        return Response({"detail": "نوبت با موفقیت به عنوان انجام شده ثبت شد."})    

class CounselorAppointmentCancelAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = request.user
        if not hasattr(user, "profile") or user.profile.role != "counselor":
            return Response({"detail": "شما مشاور نیستید."}, status=403)
        try:
            counselor = Counselor.objects.get(user=user)
        except Counselor.DoesNotExist:
            return Response({"detail": "پروفایل مشاور یافت نشد."}, status=404)
        try:
            appointment = Appointment.objects.get(id=pk, counselor=counselor)
        except Appointment.DoesNotExist:
            return Response({"detail": "نوبت یافت نشد."}, status=404)
        appointment.status = "canceled"
        appointment.save()
        return Response({"detail": "نوبت با موفقیت لغو شد."})
    
class PublicPostListAPI(generics.ListAPIView):
    queryset = Post.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = PostSerializer

class CreatePostAPI(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.profile.role not in ["author", "admin", "counselor"]:
            raise PermissionDenied("اجازه دسترسی ندارید")
        serializer.save(author=self.request.user)
    

class UpdatePostAPI(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        if self.request.user != post.author and self.request.user.profile.role != "admin":
            raise PermissionDenied("شما مالک این پست نیستید")
        serializer.save()

class DeletePostAPI(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user

        if user.profile.role != "admin" and instance.author != user:
            raise PermissionDenied("اجازه حذف این پست را ندارید")

        instance.delete()

class MyPostsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class MyPostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
class BlogPostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all().filter(is_published=True)
        return queryset.order_by("-created_at")

class BlogPostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.all()

class ClientProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user