from django.contrib import admin
from .models import SupportCase, Feedback, Response, Profile

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
    list_display = ('id', 'case', 'agent', 'responded_at')
    list_filter = ('responded_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

