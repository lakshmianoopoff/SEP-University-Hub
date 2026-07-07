from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, Course, Student
from .forms import StudentForm


class AcademicViewsAndFormsTestCase(TestCase):
    def setUp(self):
        # Create a sample department and course for the tests
        self.dept = Department.objects.create(
            name="Computer Science",
            head_of_dept="Dr. Alan Turing",
            description="Department of Computer Science and Engineering"
        )
        self.course = Course.objects.create(
            department=self.dept,
            name="Web Development",
            code="CS101",
            semester=1,
            credits=4
        )

    def test_hello_world_view(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, World!")

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Web Development")
        self.assertContains(response, "CS101")
        self.assertContains(response, "Computer Science")

    def test_student_form_validation(self):
        # Test validation fails with non-university email
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@gmail.com',
            'courses': [self.course.id]
        }
        form = StudentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "Only university emails are allowed.")

        # Test validation passes with university email
        form_data_valid = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@university.edu',
            'courses': [self.course.id]
        }
        form_valid = StudentForm(data=form_data_valid)
        self.assertTrue(form_valid.is_valid())

    def test_student_creation_post_redirect_get(self):
        form_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@university.edu',
            'courses': [self.course.id]
        }
        response = self.client.post(reverse('student_create'), data=form_data)
        # Check that it redirects to course_list
        self.assertRedirects(response, reverse('course_list'))
        
        # Check that Student is saved in the database
        student = Student.objects.get(email='alice.smith@university.edu')
        self.assertEqual(student.first_name, 'Alice')
        self.assertEqual(student.last_name, 'Smith')

    def test_user_registration_view(self):
        # GET request
        response = self.client.get(reverse('register_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        # POST request (creating a user)
        user_data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        response = self.client.post(reverse('register_user'), data=user_data)
        self.assertRedirects(response, reverse('login'))
        
        # Verify user is created
        self.assertTrue(User.objects.filter(username='newuser').exists())
