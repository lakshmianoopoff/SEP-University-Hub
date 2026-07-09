from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import StudentForm
from .models import Course

from rest_framework import viewsets
from .models import Course, Student

from .serializers import *


# This ONE class handles GET (List), GET (Detail), POST, PUT, and DELETE
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


def api_course_list(request):
    courses=Course.objects.all()
    
    data={
        'count': courses.count(),
        'results':list(courses.values('name','code','credits'))
    }
    return JsonResponse(data)


def hello_world(request):
    return HttpResponse("Hello, World!")



def student_create(request):

    if request.method == 'POST':
        # 1. Bind data to the form
        form = StudentForm(request.POST)

        # 2. Validation Check
        if form.is_valid():
           # get login fields safely
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            email = request.POST.get('email', '').strip()
             

            if not username or not password or not email:
                return render(
                    request,
                    'academic/student_form.html',
                    {
                        'form': form,
                        'error': 'All login fields required'
                    }
                )
            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    'academic/student_form.html',
                    {
                        'form': form,
                        'error': 'Username already exists'
                    }
                )

            # create user first
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

  # THEN create student object
            student = form.save(commit=False)
            student.user = user
            student.save()

            form.save_m2m()

            return redirect('course_list')

         # 4. Redirect (Post-Redirect-Get Pattern)
            return redirect('course_list')

    else:
        # GET request: Create empty form
        form = StudentForm()

    return render(
        request,
        'academic/student_form.html',
        {'form': form}
    )

@login_required
def course_list(request):
    # 1. Fetch data from DB
    all_courses = Course.objects.all()

    # 2. Context: A dictionary mapping template variable names to Python objects
    context = {
        'courses': all_courses,
        'page_title': 'Available Courses'
    }

    # 3. Render: Combine the request, the template, and the data
    return render(request, 'academic/course_list.html', context)

def is_admin(user):
    return user.is_staff
def delete_student(request,id):
    student = student.objects.get(id=id)
    if student.user:
        student.user.delete()
    else:
        student.delete()
    return redirect('course_list')


def register_user(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


@login_required
def student_profile(request,id):
    profile=Student.objects.get(id=id)

    if request.user!=profile.user:
        return HttpResponseForbidden("You are not authorized to view this profile.")
    return HttpResponse("Profile allowed")

