from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'


class CourseSerializer(serializers.ModelSerializer):
 class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'credits', 'department', 'semester']


# 3. Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'courses','profile_pic']