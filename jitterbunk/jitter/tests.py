from django.test import TestCase, Client
from django.urls import reverse

from .models import Bunk, User

class UserTests(TestCase):
    
    def test_signup_page_basic(self):
        client = Client()

        # test username is required
        response = client.post(reverse('jitter:signup'))
        self.assertEqual(response.context['error_msg'], 'username is required - please enter a username')

        # test password is required
        response = client.post(reverse('jitter:signup'), {'username': 'testname1'})
        self.assertEqual(response.context['error_msg'], 'password is required - please enter a password')

        # test can create user from username and password
        response = client.post(reverse('jitter:signup'), {'username': 'testname1', 'password': 'abc123abc123'})
        
        try:
            u = User.objects.get(username='testname1')
        except:
            self.fail('signup did not create user')
        else: 
            # test that you can't create two users with the same username 
            response = client.post(reverse('jitter:signup'), {'username': 'testname1', 'password': 'abc123abc123'})
            self.assertEqual(response.context['error_msg'], 'user already exists - enter a different username')

            # test original user was logged in
            self.assertTrue(u.logged_in)
            u.delete()
        
    def test_signup_page_all_fields(self):
        client = Client()

        # test that you can create user with all fields
        client.post(reverse('jitter:signup'), 
            {
                'username': 'testname1', 
                'password': 'abc123abc123',
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',
                'photo_url': 'https://test_image.png'
            })
        try:
            u = User.objects.get(username='testname1')
        except:
            self.fail('signup did not create user')
        else: 
            self.assertTrue(u.logged_in)
            self.assertEqual(u.first_name, 'test')
            self.assertEqual(u.last_name, 'user')
            self.assertEqual(u.photo, 'https://test_image.png')
            u.delete()
    
    def test_login_page(self):
        client = Client()
        
        u = User.objects.create(username='testname1', password='abc123abc123')
        u.set_password('abc123abc123')
        u.save()

        # test can't login with only a username
        response = client.post(reverse('jitter:login'), {'username': 'testname1'})
        self.assertEqual(response.context['error_msg'], 'unable to authenticate user - enter a correct username and password')

        # test can't login with only a password
        response = client.post(reverse('jitter:login'), {'password': 'abc123abc123'})
        self.assertEqual(response.context['error_msg'], 'unable to authenticate user - enter a correct username and password')

        # test that user can login and be redirected to their personal page
        response = client.post(reverse('jitter:login'), {'username': 'testname1', 'password': 'abc123abc123'})
        self.assertEqual(response['Location'], '/jitter/testname1/personal_feed')
        u.delete()

