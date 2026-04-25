from django.contrib import admin
from .models import (
    Profile, Counselor, Test, Appointment,
    TestResult, BlogPost, Feedback, DiscountCode, Transaction
)

# ----------------------
# Profile Admin
# ----------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    search_fields = ("user__username", "phone")
    list_filter = ("role",)


# ----------------------
# Counselor Admin
# ----------------------
@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ("user", "specialties", "rating", "rating_count")
    search_fields = ("user__username", "specialties")
    list_filter = ("rating",)


# ----------------------
# Test Admin
# ----------------------
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "is_prerequisite")
    search_fields = ("title",)
    list_filter = ("is_prerequisite",)


# ----------------------
# Appointment Admin
# ----------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "counselor",
        "start_time",
        "end_time",
        "status",
        "price",
        "is_paid",
    )
    search_fields = ("client__username", "counselor__user__username")
    list_filter = ("status", "is_paid", "counselor")
    ordering = ("-start_time",)


# ----------------------
# Test Result Admin
# ----------------------
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "created_at")
    search_fields = ("user__username", "test__title")
    list_filter = ("test", "created_at")


# ----------------------
# Blog Post Admin
# ----------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


# ----------------------
# Feedback Admin
# ----------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "counselor", "rating", "created_at")
    search_fields = ("user__username", "counselor__user__username")
    list_filter = ("rating", "created_at")


# ----------------------
# Discount Code Admin
# ----------------------
@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "percent", "active")
    search_fields = ("code",)
    list_filter = ("active",)


# ----------------------
# Transaction Admin
# ----------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "successful", "created_at")
    search_fields = ("user__username", "gateway_tracking_code")
    list_filter = ("successful", "created_at")
    ordering = ("-created_at",)
