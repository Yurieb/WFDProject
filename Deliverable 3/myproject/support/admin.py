from django.contrib import admin
from .models import SupportCase, Feedback, Response, Profile

@admin.register(SupportCase)
class SupportCaseAdmin(admin.ModelAdmin):
    # Show key fields to help admins quickly view case details
    list_display = ('id', 'subject', 'status', 'customer', 'agent', 'created_at')
    list_filter = ('status', 'created_at')  # Easy filtering by status or date
    search_fields = ('subject', 'description')  # Allow searching by case content

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'rating', 'submitted_at')
    list_filter = ('rating',)  # Helpful for sorting by satisfaction scores

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'agent', 'responded_at')
    list_filter = ('responded_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)  # Filter users by role Customer, Agent, Manager
    search_fields = ('user__username',)  # Quick search by username
