from django.contrib import admin
from .models import Customer, Agent, SupportCase, Feedback, Response

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email') 

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role') 
    search_fields = ('name', 'email', 'role')

@admin.register(SupportCase)
class SupportCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'customer', 'agent', 'created_at') 
    list_filter = ('status', 'created_at') 
    search_fields = ('subject', 'description')   

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'rating', 'submitted_at') 
    list_filter = ('rating',) 

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'agent', 'responded_at')  # Show response details
    list_filter = ('responded_at',)      