from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.test import TestCase
from ..views import new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm
from django.contrib.auth.models import User

class NewTopicTests(TestCase):
    def setUp(self):
        # print("\nTest new topic")
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  # <- included this line here

    
    def test_new_topic_view_success_status_code(self):
        # print("\nTest new topic view success status code")
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_new_topic_view_not_found_status_code(self):
        # print("\nTest new topic view not found status code")
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_new_topic_url_resolves_new_topic_view(self):
        # print("\nTest new topic url resolves new topic view")
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)
    
    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        # print("\nTest new topic view contains link back to board topics view")
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        # print("\nTest csrf")
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_new_topic_valid_post_data(self):
        # print("\nTest new topic valid post data")
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_new_topic_invalid_post_data(self):
        # print("\nTest new topic invalid post data")
        ''''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        # print("\nTest new topic invalid post data empty fields")
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
    def test_contains_form(self):
        # print("\nTest contains form")
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))