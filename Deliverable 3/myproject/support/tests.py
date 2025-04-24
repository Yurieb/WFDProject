from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import SupportCase, Response, Feedback, Profile
from django.urls import reverse

class SupportSystemTests(TestCase):

    def setUp(self):
        # Create test users with roles: Customer, Agent, Manager
        self.customer = User.objects.create_user(username='customer', password='pass123')
        Profile.objects.create(user=self.customer, role='Customer')

        self.agent = User.objects.create_user(username='agent', password='pass123')
        Profile.objects.create(user=self.agent, role='Agent')

        self.manager = User.objects.create_user(username='manager', password='pass123')
        Profile.objects.create(user=self.manager, role='Manager')
         # Set up Django test client for simulating requests
        self.client = Client()

    def test_submit_support_case(self):
        """Customer submits a support case"""
        self.client.login(username='customer', password='pass123')
        response = self.client.post(reverse('submit_case'), {
            'subject': 'Test Subject',
            'description': 'Test description here.'
        })
        self.assertEqual(response.status_code, 302)  #
        self.assertEqual(SupportCase.objects.count(), 1)
         # Create a case that will be assigned
    def test_assign_agent(self):
        """Manager assigns an agent to a case"""
        case = SupportCase.objects.create(customer=self.customer, subject='Test', description='Desc')
        self.client.login(username='manager', password='pass123')
        response = self.client.post(reverse('assign_agent', args=[case.id]), {
            'agent_id': self.agent.id
        })
        case.refresh_from_db()
        self.assertEqual(case.agent, self.agent)
        self.assertEqual(response.status_code, 302)

        # assign the agent to the case
    def test_agent_responds_to_case(self):
        """Agent responds to an open case and it gets closed"""
        case = SupportCase.objects.create(customer=self.customer, subject='Test', description='Desc', agent=self.agent)
        self.client.login(username='agent', password='pass123')
        response = self.client.post(reverse('add_response', args=[case.id]), {
            'message': 'We will fix this soon.'
        })
        case.refresh_from_db()
        self.assertEqual(Response.objects.count(), 1)
        self.assertEqual(case.status, 'closed')

         # Create a closed case so feedback can be submitted
    def test_customer_gives_feedback(self):
        """Customer gives feedback after case is closed"""
        case = SupportCase.objects.create(customer=self.customer, subject='Test', description='Desc', status='closed')
        self.client.login(username='customer', password='pass123')
        response = self.client.post(reverse('give_feedback', args=[case.id]), {
            'rating': 5,
            'comments': 'Great help!'
        })
        self.assertEqual(response.status_code, 302) # Check redirect after feedback
        self.assertEqual(Feedback.objects.count(), 1)  # Ensure feedback was stored
