from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_case, name='submit_case'),
    path('cases/', views.case_list, name='case_list'),
]

