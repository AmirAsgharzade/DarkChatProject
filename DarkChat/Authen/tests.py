from django.test import TestCase
from .models import CustomUser
from .forms import LoginForm,RegisterForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
# Create your tests here.

# Unit Tests
#model_test
class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(username='testUser',password='testpass')
        self.assertEqual(user.username,'testUser')
    
    def test_unique_username(self):
        CustomUser.objects.create_user(username='testUser',password='testpass')
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(username='testUser',password='testpass')


#form_test
class LoginFromTest(TestCase):
    def test_login_form_valid(self):
        form = LoginForm(data={'username':'testuser','password':'testpass'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username':'user','password':'pass'})
        self.assertFalse(form.is_valid())

#form-test
class RegisterFormTest(TestCase):
    def test_register_form_vaild(self):
        form = RegisterForm(data={'username':'testuser','password':'testpass','password_confirm':'testpass'})
        self.assertTrue(form.is_valid())
    
    def test_register_form_invalid(self):
        form = RegisterForm(data={'username':'','password':'test','password_confirm':'test'})
        self.assertFalse(form.is_valid())
    
    def test_register_clean_form(self):
        form = RegisterForm(data={'username':'testuser','password':'testuesr1','password_confirm':'testuser2'})
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.clean()
    
    def test_register_save(self):
        form = RegisterForm(data={'username':'testuser','password':'testpass','password_confirm':'testpass'})
        self.assertTrue(form.save())



#Integration Test
#Auth Test
class UserAuthTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('Authen.register'),{'username':'testuser','password':'testpass','password_confirm':'testpass'})
        self.assertEqual(response.status_code,302)
    
    def test_user_login(self):
        self.client.post(reverse('Authen.register'),{'username':'testuser','password':'testpass','password_confirm':'testpass'})
        response = self.client.post(reverse('Authen.login'),{'username':'testuser','password':'testpass'})
        self.assertEqual(response.status_code,302)
