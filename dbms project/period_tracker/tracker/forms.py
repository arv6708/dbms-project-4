from django import forms
from .models import Cycle, Symptom, Mood, DailyLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['start_date', 'end_date', 'cycle_length', 'period_length', 'average_flow', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['cycle', 'date', 'symptom_type', 'severity', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['cycle', 'date', 'mood_type', 'intensity', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['date', 'flow_level', 'mood', 'symptoms', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'symptoms': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }