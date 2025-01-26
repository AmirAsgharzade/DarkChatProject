from django.test import TestCase
from .models import GlobeHistory,CustomUser
from django.urls import reverse

# Create your tests here.

#Unit Test
class GlobeHistoryTest(TestCase):
    def test_chat_message_creation(self):
         user = CustomUser.objects.create_user(username='testuser', password='testpass')
         message = GlobeHistory.objects.create(user=user,username=user.username,color=user.color,content='Hello World!')
         self.assertEqual(message.content,'Hello World!')
    
    def test_message_timestamp(self):
        user = CustomUser .objects.create_user(username='testuser', password='testpass')
        chat = GlobeHistory.objects.create(user=user, username=user.username,color=user.color,content='Hello, World!')
        self.assertIsNotNone(chat.timestamp)  # Assuming you have a timestamp field


class IndexViewTest(TestCase):

    def test_unauthorized_access(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
