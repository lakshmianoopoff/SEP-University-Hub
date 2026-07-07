from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentForm
from .models import Course


def hello_world(request):
    return HttpResponse("Hello, World!")


def student_create(request):

    if request.method == 'POST':
        # 1. Bind data to the form
        form = StudentForm(request.POST)

        # 2. Validation Check
        if form.is_valid():
            # 3. Save to DB
            form.save()

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