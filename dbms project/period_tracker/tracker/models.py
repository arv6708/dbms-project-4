from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cycle(models.Model):
    FLOW_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
        ('none', 'None'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cycle_length = models.IntegerField(help_text="Length of cycle in days")
    period_length = models.IntegerField(help_text="Length of period in days")
    average_flow = models.CharField(max_length=10, choices=FLOW_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username}'s cycle starting {self.start_date}"

class DailyLog(models.Model):
    FLOW_LEVELS = [
        ('none', 'No Flow'),
        ('spotting', 'Spotting'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    flow_level = models.CharField(max_length=10, choices=FLOW_LEVELS, default='none')
    mood = models.CharField(max_length=20, blank=True)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.flow_level}"

class Symptom(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField()
    symptom_type = models.CharField(max_length=100)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.symptom_type} on {self.date}"

class Mood(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('anxious', 'Anxious'),
        ('energetic', 'Energetic'),
        ('tired', 'Tired'),
        ('irritable', 'Irritable'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    date = models.DateField()
    mood_type = models.CharField(max_length=20, choices=MOOD_CHOICES)
    intensity = models.IntegerField(help_text="Intensity from 1-10")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.mood_type} on {self.date}"