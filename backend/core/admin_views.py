from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import Appointment, Counselor, Transaction, Profile, Post
from django.db.models import Count, Sum
from .serializers import (AdminAppointmentSerializer, 
            AdminUserSerializer, AdminCounselorSerializer, AdminUserRoleSerializer,
            PostSerializer)

class AdminStatsAPI(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        return Response({
            "users": User.objects.count(),
            "counselors": Counselor.objects.count(),
            "appointments": Appointment.objects.count(),
            "income": Transaction.objects.filter(successful=True).aggregate(Sum("amount"))["amount__sum"] or 0,
            "status_counts": Appointment.objects.values("status").annotate(total=Count("id")),
        })

class AdminUsersListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)
        return super().list(request, *args, **kwargs)


class AdminUserDeleteAPI(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)
        if user.is_staff:
            return Response(
                {"detail": "نمی‌توان ادمین‌ها را حذف کرد."},
                status=400
            )
        if user.id == request.user.id:
            return Response(
                {"detail": "نمی‌توان کاربری که وارد شده را حذف کرد."},
                status=400
            )
        return super().delete(request, *args, **kwargs)
    
class AdminCounselorListAPI(generics.ListAPIView):
    queryset = Counselor.objects.all()
    serializer_class = AdminCounselorSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)
        return super().list(request, *args, **kwargs)


class AdminCounselorToggleAPI(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)

        try:
            counselor = Counselor.objects.get(id=pk)
        except Counselor.DoesNotExist:
            return Response({"detail": "مشاور یافت نشد"}, status=404)

        counselor.is_active = not counselor.is_active
        counselor.save()

        return Response({"detail": "وضعیت تغییر یافت"})

class AdminAppointmentsListAPI(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)
        return super().list(request, *args, **kwargs)


class AdminAppointmentUpdateAPI(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)
        return super().update(request, *args, **kwargs, partial=True)

class AdminUserRoleUpdateAPI(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "دسترسی غیرمجاز"}, status=403)

        user = get_object_or_404(User, pk=pk)
        profile = getattr(user, "profile", None)
        if profile is None:
            return Response({"detail": "پروفایل یافت نشد"}, status=404)

        serializer = AdminUserRoleSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.validated_data.get("role") == "counselor":
            from .models import Counselor
            Counselor.objects.get_or_create(user=user)
        
        if serializer.validated_data.get("role") == "client":
            from .models import Counselor
            Counselor.objects.filter(user=user).delete()

        return Response(serializer.data, status=200)

class AdminPostListAPI(generics.ListAPIView):
    """
    لیست همه پست‌ها برای پنل ادمین
    GET /admin/posts/
    """
    queryset = Post.objects.all().select_related("author").order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class AdminPostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    مدیریت یک پست خاص برای ادمین:
    - GET /admin/posts/<id>/
    - PATCH /admin/posts/<id>/
    - DELETE /admin/posts/<id>/
    """
    queryset = Post.objects.all().select_related("author")
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

class CounselorStatsAPI(APIView):
    def get(self, request):
        counselors = Profile.objects.filter(role="counselor")

        data = []

        for c in counselors:
            b = Counselor.objects.filter(user=c.user).first()
            data.append({
                "username": b.user.username,
                "pending": Appointment.objects.filter(counselor=b, status="pending").count(),
                "done": Appointment.objects.filter(counselor=b, status="done").count(),
                "cancelled": Appointment.objects.filter(counselor=b, status="cancelled").count(),
            })

        return Response(data)