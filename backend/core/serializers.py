from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Counselor, Test, Appointment, TestResult,
    BlogPost, Feedback, Post
)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", 'is_staff', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class CounselorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Counselor
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    counselor = serializers.PrimaryKeyRelatedField(queryset=Counselor.objects.all())
    counselor_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["status", "is_paid", "end_time"]

    def get_counselor_info(self, obj):
        if not obj.counselor or not obj.counselor.user:
            return None

        user = obj.counselor.user
        full_name = f"{user.first_name} {user.last_name}".strip()

        return {
            "id": obj.counselor.id,
            "username": user.username,
            "full_name": full_name or user.username,
        }


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = BlogPost
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

class CounselorProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    specialties = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        user = instance
        profile = user.profile
        counselor = user.counselor

        # Update user
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.save()

        # Update profile
        profile.phone = validated_data.get("phone", profile.phone)
        profile.bio = validated_data.get("bio", profile.bio)
        profile.save()

        # Update counselor table
        counselor.specialties = validated_data.get("specialties", counselor.specialties)
        counselor.resume = validated_data.get("resume", counselor.resume)
        counselor.save()

        return user

class CounselorAppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.username", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "client_name",
            "start_time",
            "end_time",
            "status",
            "is_paid",
        ]


class AdminUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class AdminCounselorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Counselor
        fields = ["id", "full_name", "specialties"]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()


class AdminAppointmentSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    counselor = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ["id", "client", "counselor", "start_time", "status"]

    def get_client(self, obj):
        return obj.client.username

    def get_counselor(self, obj):
        return obj.counselor.user.username

class AdminUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["role"]

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]