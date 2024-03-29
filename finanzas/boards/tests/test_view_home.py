from django.urls import reverse, resolve
from django.test import TestCase
from ..models import Board
from ..views import home
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        # print("\nTest home view status code")
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        # print("\nTest home url resolves home view")
        view = resolve('/')
        self.assertEquals(view.func, home)
    
    class HomeTests(TestCase):
        def setUp(self):
            self.board = Board.objects.create(name='Django', description='Django board.')
            url = reverse('home')
            self.response = self.client.get(url)

        def test_home_view_contains_link_to_topics_page(self):
            # print("\nTest home view contains link to topics page")
            board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
            self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

