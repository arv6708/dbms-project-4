from django.contrib import admin
from .models import Cycle, Symptom, Mood, DailyLog

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'cycle_length', 'period_length', 'average_flow']
    list_filter = ['start_date', 'average_flow', 'user']
    search_fields = ['user__username', 'notes']

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['user', 'cycle', 'date', 'symptom_type', 'severity']
    list_filter = ['symptom_type', 'severity', 'date']
    search_fields = ['user__username', 'symptom_type', 'description']

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'cycle', 'date', 'mood_type', 'intensity']
    list_filter = ['mood_type', 'date']
    search_fields = ['user__username', 'mood_type', 'notes']

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'flow_level', 'mood']
    list_filter = ['flow_level', 'date', 'user']
    search_fields = ['user__username', 'mood', 'symptoms', 'notes']