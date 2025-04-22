from django.db import models
from django.contrib.auth.models import User

# Customer model represents the customers who submit support cases
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Agent model represents  the support agents and managers    
class Agent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('agent', 'Agent'), ('manager', 'Manager')], default='agent')

    def __str__(self):
        return self.name
    
# SupportCase model represents the support issues submitted by customers
class SupportCase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# Response model represents agent responses to cases
class Response(models.Model):
    case = models.ForeignKey(SupportCase, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    message = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)


# Feedback model represents feedback left by customers after case is handled
class Feedback(models.Model):
    case = models.ForeignKey(SupportCase, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

# Each user has a role: Customer, Agent, or Manager
# Role is used to control what the user can do in the system
class Profile(models.Model):
    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Agent', 'Agent'),
        ('Manager', 'Manager'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"    

