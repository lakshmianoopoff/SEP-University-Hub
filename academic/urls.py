from django.urls import path
from academic import views


urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('courses/', views.course_list, name='course_list'),
    path('register-student/', views.student_create, name='student_create'),
    path('register/', views.register_user, name='register_user'),
]