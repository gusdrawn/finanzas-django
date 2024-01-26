from django.test import TestCase
from ..forms import SignUpForm
from django.urls import reverse, resolve
from ..views import signup
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpTests(TestCase):
    def setUp(self):
        print("\nTest sign up")
        url = reverse('signup')
        self.response = self.client.get(url)
    
    def test_signup_status_code(self):
        print("\nTest signup status code")
        self.assertEquals(self.response.status_code, 200)
    
    def test_signup_url_resolves_signup_view(self):
        print("\nTest signup url resolves signup view")
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)
    
    def test_csrf(self):
        print("\nTest csrf")
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        print("\nTest contains form")
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        print("\nTest form inputs")
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    def test_redirection(self):
        print("\nTest redirection")
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        print("\nTest user creation")
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        print("\nTest user authentication")
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
    
    def test_signup_status_code(self):
        print("\nTest signup status code")
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)
    
    def test_form_errors(self):
        print("\nTest form errors")
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        print("\nTest don't create user")
        self.assertFalse(User.objects.exists())