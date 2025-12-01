from django.urls import path
from . import views

urlpatterns = [
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Student URLs
    path("students/", views.view_students, name="view_students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:student_id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),

    # Faculty URLs
    path("faculty/", views.view_faculty, name="view_faculty"),
    path("faculty/add/", views.add_faculty, name="add_faculty"),
    path("faculty/edit/<int:faculty_id>/", views.edit_faculty, name="edit_faculty"),
    path("faculty/delete/<int:faculty_id>/", views.delete_faculty, name="delete_faculty"),

    # Logout
    path("logout/", views.admin_logout, name="admin_logout"),
]
