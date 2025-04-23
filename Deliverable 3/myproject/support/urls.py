from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_case, name='submit_case'),
    path('cases/', views.case_list, name='case_list'),
    path('register/', views.register, name= 'register'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('assign/<int:case_id>/', views.assign_agent, name='assign_agent'),
    path('response/<int:case_id>/', views.add_response, name='add_response'),
    path('feedback/<int:case_id>/', views.give_feedback, name='give_feedback'),
]

