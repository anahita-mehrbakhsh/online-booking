from django.urls import path
from .admin_views import (
    AdminStatsAPI,
    AdminUsersListAPI, AdminUserDeleteAPI,
    AdminCounselorListAPI, AdminCounselorToggleAPI,
    AdminAppointmentsListAPI, AdminAppointmentUpdateAPI, AdminUserRoleUpdateAPI,
    AdminPostListAPI, AdminPostDetailAPI, CounselorStatsAPI
)
from .views import (
    RegisterAPI, LoginAPI, CounselorListAPI, CounselorDetailAPI,
    TestListAPI, BlogListAPI, BlogDetailAPI,
    AppointmentListCreateAPI, TestResultAPI, FeedbackAPI, ProfileAPI,
    CounselorProfileAPI, CounselorAppointmentsAPI,
    CounselorAppointmentMarkDoneAPI, CounselorAppointmentCancelAPI, MyPostsAPI, CreatePostAPI,
    MyPostDetailAPI, BlogPostListAPI, BlogPostDetailAPI, ClientProfileAPI
)

urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),

    path("counselors/", CounselorListAPI.as_view()),
    path("counselor/profile/", CounselorProfileAPI.as_view()),
    path("counselor/appointments/", CounselorAppointmentsAPI.as_view()),
    path("counselor/appointments/<int:pk>/done/", CounselorAppointmentMarkDoneAPI.as_view()),
    path("counselor/appointments/<int:pk>/cancel/", CounselorAppointmentCancelAPI.as_view()),
    path("counselors/<int:pk>/", CounselorDetailAPI.as_view()),

    path("tests/", TestListAPI.as_view()),

    path("blog/", BlogListAPI.as_view()),
    path("blog/<int:pk>/", BlogDetailAPI.as_view()),

    path("appointments/", AppointmentListCreateAPI.as_view()),
    path("test-result/", TestResultAPI.as_view()),
    path("feedback/", FeedbackAPI.as_view()),
    path("profile/", ProfileAPI.as_view()),
    path("admin/stats/", AdminStatsAPI.as_view()),
    path("admin/users/", AdminUsersListAPI.as_view()),
    path("admin/users/<int:pk>/", AdminUserDeleteAPI.as_view()),
    path("admin/counselors/", CounselorStatsAPI.as_view()),
    path("admin/counselors/<int:pk>/toggle/", AdminCounselorToggleAPI.as_view()),
    path("admin/appointments/", AdminAppointmentsListAPI.as_view()),
    path("admin/appointments/<int:pk>/", AdminAppointmentUpdateAPI.as_view()),
    path("admin/users/<int:pk>/role/", AdminUserRoleUpdateAPI.as_view()),
    path("admin/posts/", AdminPostListAPI.as_view()),
    path("admin/posts/<int:pk>/", AdminPostDetailAPI.as_view()),
    path("posts/", CreatePostAPI.as_view()),
    path("posts/list/", BlogPostListAPI.as_view()),
    path("posts/list/<int:pk>/", BlogPostDetailAPI.as_view()),
    path("posts/mine/", MyPostsAPI.as_view()),
    path("posts/<int:pk>/", MyPostDetailAPI.as_view()),
    path("profile/edt/", ClientProfileAPI.as_view()),


]
