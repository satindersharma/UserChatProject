import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from erpapp.models import Lead


class ListLeadByUserListView(TestCase):
    def setUp(self):
        # create two users
        test_user1 = get_user_model().objects.create_user(
            username='testuser1', password='testuser1', email='test@gmail.com')
        test_user11 = get_user_model().objects.create_user(
            username='testuser11', password='testuser11', email='test1@gmail.com')
        test_user1.save()
        test_user11.save()

        # create a lead
        # l1 = Lead.objects.create(name='abay',mobile=8787676576)

    def test_redirect_if_not_logged_in(self):
        reponse = self.client.get(reverse('erpapp:lead'))
        
        self.assertRedirects(reponse, '/login/?next=/lead/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1', email='test@gmail.com')
        response = self.client.get(reverse('home'))
        print(response)
        # self.assertEqual(str(response.context['user']), 'testuser1')
        # check that we got a  response "success"
        self.assertEqual(response.status_code, 200)

        # check we used correct template
        self.assertTemplateUsed(response, 'home.html')