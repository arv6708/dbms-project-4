from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Changed to custom view
    path('add-cycle/', views.add_cycle, name='add_cycle'),
    path('add-symptom/', views.add_symptom, name='add_symptom'),
    path('add-mood/', views.add_mood, name='add_mood'),
    path('add-daily-log/', views.add_daily_log, name='add_daily_log'),
    path('statistics/', views.statistics, name='statistics'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_month'),
    path('settings/', views.settings_view, name='settings'),
]