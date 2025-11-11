from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.db.models import Q
from .models import Message
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from .models import FacultyProfile


from django.template.loader import render_to_string






def login_view(request):
    if request.method == "POST":
        college_id = request.POST.get('college_id')
        password = request.POST.get('password')
        print("Login attempt:", college_id, password)  # 👈 Add this line


        user = authenticate(request, username=college_id, password=password)
        print("Authenticated user:", user)  # 👈 Add this line

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        college_id = request.POST.get('college_id')
        email = request.POST.get('email')
        role = request.POST.get('role')
        skills = request.POST.get('skills')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password validation
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Check if user already exists
        if UserProfile.objects.filter(college_id=college_id).exists():
            return render(request, 'register.html', {'error': 'College ID already registered'})
        if UserProfile.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered'})

        # Create User
        user = User.objects.create_user(username=college_id, password=password)
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            full_name=name,
            college_id=college_id,
            email=email,
            role=role,
            skills=skills
        )

        return redirect('login')
    
    return render(request, 'register.html')





@login_required
def main_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'main.html', {'profile': profile})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def profile_view(request):
    # Get the logged-in user's profile
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def view_other_profile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'view_other_profile.html', {'profile': profile})

def discover_skills_view(request):
    profiles = UserProfile.objects.all()  # get all user profiles
    return render(request, 'discover_skills.html', {'profiles': profiles})


def home_view(request):
    return render(request, 'home.html')
from django.contrib.auth import logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def create_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.student_id = request.POST.get('student_id')
        profile.previous_education = request.POST.get('previous_education')
        profile.current_education = request.POST.get('current_education')
        profile.department = request.POST.get('department')
        profile.about = request.POST.get('about')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')

        # For photo and certificate uploads
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        if 'certificate' in request.FILES:
            profile.certificate = request.FILES['certificate']

        profile.save()
        return redirect('profile')  # redirect to profile page after saving

    return render(request, 'create_profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get('full_name')
        profile.student_id = request.POST.get('student_id')
        profile.previous_education = request.POST.get('previous_education')
        profile.current_education = request.POST.get('current_education')
        profile.department = request.POST.get('department')
        profile.about = request.POST.get('about')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')

        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        if 'certificate' in request.FILES:
            profile.certificate = request.FILES['certificate']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})

def discover_skills_explore(request):
    query = request.GET.get('q', '')
    profiles = UserProfile.objects.all()


    if query:
        profiles = profiles.filter(
            Q(full_name__icontains=query) |
            Q(skills__icontains=query) |
            Q(department__icontains=query)
        )

    return render(request, 'discover_skills_explore.html', {
        'profiles': profiles,
        'query': query,
    })

@login_required
def send_message(request):
    error = None  # Default: no error
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            return redirect('messages')
        except User.DoesNotExist:
            error = "❌ User not found!"

    return render(request, 'send_message.html', {'error': error})


@login_required
def messages_view(request):
    user = request.user
    query = request.GET.get('q', '').strip()  # ✅ safer: handles empty input

    users = None
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(userprofile__full_name__icontains=query)
        ).exclude(id=user.id).distinct()  # ✅ avoid duplicates if any

    # ✅ Fetch messages sorted by latest first
    received = Message.objects.filter(receiver=user).order_by('-timestamp')
    sent = Message.objects.filter(sender=user).order_by('-timestamp')

    return render(request, 'messages.html', {
        'received': received,
        'sent': sent,
        'users': users,
        'query': query,
    })




@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    # Handle sending a message
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
        return HttpResponse(status=204)  # no reload needed

    # Handle AJAX refresh — return only messages partial
    if request.GET.get('ajax'):
        html = render_to_string('partials/chat_messages.html', {
            'messages': messages,
            'request': request
        })
        return HttpResponse(html)

    # Normal page load
    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages,
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query) |
        Q(userprofile__full_name__icontains=query)
    ).exclude(id=request.user.id)

    return render(request, 'search_users.html', {'users': users, 'query': query})

@login_required
def faculty_profile(request, username):
    faculty_user = get_object_or_404(User, username=username)
    faculty = get_object_or_404(UserProfile, user=faculty_user, role='faculty')
    return render(request, 'faculty_profile.html', {'faculty': faculty})

@login_required
def faculty_dashboard(request):
    profile = request.user.userprofile
    if profile.role != 'faculty':
        return redirect('home')  # prevent non-faculty users

    return render(request, 'faculty_dashboard.html', {'profile': profile})



class FacultyForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['photo', 'department', 'subjects_taught']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'full_name', 'department', 'subjects_taught', 'experience', 'skills', 'about']

@login_required
def edit_faculty(request):
    profile = request.user.userprofile

    if profile.role != 'faculty':
        messages.error(request, "Access denied: only faculty can edit this page.")
        return redirect('home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('faculty_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_faculty.html', {'form': form})


def faculty_list(request):
    faculties = UserProfile.objects.filter(role='faculty')
    return render(request, 'faculty_list.html', {'faculties': faculties})

# Create your views here.
