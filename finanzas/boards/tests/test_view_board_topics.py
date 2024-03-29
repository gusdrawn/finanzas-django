from django.urls import reverse, resolve
from django.test import TestCase
from ..views import board_topics
from ..models import Board

class BoardTopicsTests(TestCase):
    def setUp(self):
        # print("\nTest board topics")
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        # print("\nTest board topics view success status code")
        url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_board_topics_view_not_found_status_code(self):
        # print("\nTest board topics view not found status code")
        url = reverse('board_topics', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        # print("\nTest board topics url resolves board topics view")
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        # print("\nTest board topics view contains link back to homepage")
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
    
    def test_board_topics_view_contains_navigation_links(self):
        # print("\nTest board topics view contains navigation links")
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        
        response = self.client.get(board_topics_url)
        
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

