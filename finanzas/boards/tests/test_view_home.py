from django.urls import reverse, resolve
from django.test import TestCase
from ..models import Board
from ..views import home, BoardListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        # self.assertEqual(view.func, home)
        self.assertEqual(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

