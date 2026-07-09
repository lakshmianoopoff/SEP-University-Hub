from django.urls import path,include
from rest_framework.routers import DefaultRouter
from academic import views

router = DefaultRouter()

router.register(r'courses',views.CourseViewSet)
router.register(r'students',views.StudentViewSet)


urlpatterns = [

    path('hello/', views.hello_world, name='hello_world'),
    path('courses/', views.course_list, name='course_list'),
    path('register-student/', views.student_create, name='student_create'),
    path('register/', views.register_user, name='register_user'),
   # path('api/courses/',views.api_course_list, name="api_course_list"),
    # pyrefly: ignore [parse-error]
    path('api/',include(router.urls)),

]

