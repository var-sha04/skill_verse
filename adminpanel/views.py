from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile
from django.contrib.auth.models import User

# ----------------------
# Admin Login
# ----------------------
def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # Custom admin: check role in UserProfile
        if user is not None:
            try:
                if user.userprofile.role == "admin":
                    login(request, user)
                    return redirect("admin_dashboard")
            except:
                messages.error(request, "Not an admin user")
        messages.error(request, "Invalid credentials")
        return render(request, "adminpanel/admin_login.html")

    return render(request, "adminpanel/admin_login.html")


# ----------------------
# Admin Dashboard
# ----------------------
@login_required
def admin_dashboard(request):
    try:
        if request.user.userprofile.role != "admin":
            messages.error(request, "Access denied")
            return redirect("admin_login")
    except:
        messages.error(request, "Access denied")
        return redirect("admin_login")

    total_students = UserProfile.objects.filter(role="student").count()
    total_faculty = UserProfile.objects.filter(role="faculty").count()

    context = {
        "total_students": total_students,
        "total_faculty": total_faculty,
    }
    return render(request, "adminpanel/dashboard.html", context)


# ----------------------
# Student Management
# ----------------------
@login_required
def view_students(request):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")
    students = UserProfile.objects.filter(role="student")
    return render(request, "adminpanel/view_students.html", {"students": students})


@login_required
def add_student(request):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        college_id = request.POST.get("college_id")
        department = request.POST.get("department")
        password = request.POST.get("password")

        if User.objects.filter(username=college_id).exists():
            messages.error(request, "College ID already exists")
            return redirect("add_student")

        user = User.objects.create_user(username=college_id, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            college_id=college_id,
            email=email,
            role="student",
            department=department,
        )
        messages.success(request, "Student added successfully")
        return redirect("view_students")

    return render(request, "adminpanel/add_student.html")


@login_required
def edit_student(request, student_id):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    student = get_object_or_404(UserProfile, id=student_id, role="student")

    if request.method == "POST":
        student.full_name = request.POST.get("full_name")
        student.email = request.POST.get("email")
        student.department = request.POST.get("department")
        student.save()

        student.user.email = student.email
        student.user.save()
        messages.success(request, "Student updated successfully")
        return redirect("view_students")

    return render(request, "adminpanel/edit_student.html", {"student": student})


@login_required
def delete_student(request, student_id):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    student = get_object_or_404(UserProfile, id=student_id, role="student")
    student.user.delete()  # deletes associated User
    messages.success(request, "Student deleted successfully")
    return redirect("view_students")


# ----------------------
# Faculty Management
# ----------------------
@login_required
def view_faculty(request):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")
    faculty_list = UserProfile.objects.filter(role="faculty")
    return render(request, "adminpanel/view_faculty.html", {"faculty_list": faculty_list})


@login_required
def add_faculty(request):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        college_id = request.POST.get("college_id")
        department = request.POST.get("department")
        password = request.POST.get("password")

        if User.objects.filter(username=college_id).exists():
            messages.error(request, "Faculty ID already exists")
            return redirect("add_faculty")

        user = User.objects.create_user(username=college_id, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            college_id=college_id,
            email=email,
            role="faculty",
            department=department,
        )
        messages.success(request, "Faculty added successfully")
        return redirect("view_faculty")

    return render(request, "adminpanel/add_faculty.html")


@login_required
def edit_faculty(request, faculty_id):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    faculty = get_object_or_404(UserProfile, id=faculty_id, role="faculty")

    if request.method == "POST":
        faculty.full_name = request.POST.get("full_name")
        faculty.email = request.POST.get("email")
        faculty.department = request.POST.get("department")
        faculty.save()

        faculty.user.email = faculty.email
        faculty.user.save()
        messages.success(request, "Faculty updated successfully")
        return redirect("view_faculty")

    return render(request, "adminpanel/edit_faculty.html", {"faculty": faculty})


@login_required
def delete_faculty(request, faculty_id):
    if request.user.userprofile.role != "admin":
        return redirect("admin_login")

    faculty = get_object_or_404(UserProfile, id=faculty_id, role="faculty")
    faculty.user.delete()
    messages.success(request, "Faculty deleted successfully")
    return redirect("view_faculty")


# ----------------------
# Admin Logout
# ----------------------
@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("admin_login")
