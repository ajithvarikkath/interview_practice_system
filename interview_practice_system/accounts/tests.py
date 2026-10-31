from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.profile_url = reverse('accounts:profile')
        self.username = 'testcoder'
        self.email = 'test@example.com'
        self.password = 'SecurePass123!'
        
    def test_signup_view_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_successful(self):
        payload = {
            'username': self.username,
            'email': self.email,
            'experience_level': 'Beginner',
            'focus_area': 'Software Engineering',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(self.signup_url, payload)
        
        # Successful signup redirects to dashboard:home
        self.assertRedirects(response, reverse('dashboard:home'))
        
        # Verify user is created in database
        self.assertTrue(User.objects.filter(username=self.username).exists())
        
        # Verify custom fields are saved correctly
        user = User.objects.get(username=self.username)
        self.assertEqual(user.experience_level, 'Beginner')
        self.assertEqual(user.focus_area, 'Software Engineering')

    def test_signup_duplicate_email(self):
        # Create an existing user
        User.objects.create_user(username='olduser', email=self.email, password=self.password)
        
        payload = {
            'username': self.username,
            'email': self.email, # Duplicate email
            'experience_level': 'Beginner',
            'focus_area': 'Software Engineering',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(self.signup_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'A user with that email already exists.')

    def test_login_successful(self):
        # Pre-create user
        User.objects.create_user(username=self.username, email=self.email, password=self.password)
        
        payload = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.login_url, payload)
        self.assertRedirects(response, reverse('dashboard:home'))

    def test_login_invalid(self):
        payload = {
            'username': 'wronguser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, 200)
        # Check that error is in context or messages
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password. Please try again.")

    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_profile_update_successful(self):
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.client.login(username=self.username, password=self.password)
        
        payload = {
            'first_name': 'Test',
            'last_name': 'Coder',
            'email': 'new_email@example.com',
            'bio': 'Updated professional developer bio.',
            'experience_level': 'Advanced',
            'focus_area': 'System Design',
        }
        response = self.client.post(self.profile_url, payload)
        self.assertRedirects(response, self.profile_url)
        
        # Verify db changes
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'Coder')
        self.assertEqual(user.email, 'new_email@example.com')
        self.assertEqual(user.bio, 'Updated professional developer bio.')
        self.assertEqual(user.experience_level, 'Advanced')
        self.assertEqual(user.focus_area, 'System Design')
