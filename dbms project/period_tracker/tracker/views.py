from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta, datetime
from calendar import monthrange
from django.contrib import messages
from .models import Cycle, Symptom, Mood, DailyLog
from .forms import CycleForm, SymptomForm, MoodForm, CustomUserCreationForm, DailyLogForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

def dashboard(request):
    # If user is not authenticated, show landing page
    if not request.user.is_authenticated:
        return render(request, 'tracker/landing.html')
    
    # Get user's cycles for authenticated users
    cycles = Cycle.objects.filter(user=request.user).order_by('-start_date')[:5]
    
    total_cycles = Cycle.objects.filter(user=request.user).count()
    
    if total_cycles > 0:
        avg_cycle_length = Cycle.objects.filter(user=request.user).aggregate(
            Avg('cycle_length')
        )['cycle_length__avg']
        
        avg_period_length = Cycle.objects.filter(user=request.user).aggregate(
            Avg('period_length')
        )['period_length__avg']
    else:
        avg_cycle_length = 0
        avg_period_length = 0
    
    last_cycle = Cycle.objects.filter(user=request.user).order_by('-start_date').first()
    if last_cycle:
        next_period_start = last_cycle.start_date + timedelta(days=last_cycle.cycle_length)
        days_until_next = (next_period_start - timezone.now().date()).days
    else:
        next_period_start = None
        days_until_next = None
    
    context = {
        'cycles': cycles,
        'total_cycles': total_cycles,
        'avg_cycle_length': round(avg_cycle_length, 1) if avg_cycle_length else 0,
        'avg_period_length': round(avg_period_length, 1) if avg_period_length else 0,
        'next_period_start': next_period_start,
        'days_until_next': days_until_next,
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def add_cycle(request):
    if request.method == 'POST':
        form = CycleForm(request.POST)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.user = request.user
            cycle.save()
            return redirect('dashboard')
    else:
        form = CycleForm()
    return render(request, 'tracker/cycle_form.html', {'form': form})

@login_required
def add_symptom(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.user = request.user
            symptom.save()
            return redirect('dashboard')
    else:
        form = SymptomForm()
        form.fields['cycle'].queryset = Cycle.objects.filter(user=request.user)
    return render(request, 'tracker/symptom_form.html', {'form': form})

@login_required
def add_mood(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('dashboard')
    else:
        form = MoodForm()
        form.fields['cycle'].queryset = Cycle.objects.filter(user=request.user)
    return render(request, 'tracker/mood_form.html', {'form': form})

@login_required
def add_daily_log(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            daily_log = form.save(commit=False)
            daily_log.user = request.user
            
            # Check if log already exists for this date
            existing_log = DailyLog.objects.filter(
                user=request.user, 
                date=daily_log.date
            ).first()
            
            if existing_log:
                # Update existing log
                existing_log.flow_level = daily_log.flow_level
                existing_log.mood = daily_log.mood
                existing_log.symptoms = daily_log.symptoms
                existing_log.notes = daily_log.notes
                existing_log.save()
            else:
                daily_log.save()
            
            return redirect('calendar')
    else:
        initial_date = request.GET.get('date', timezone.now().date())
        # Check if log already exists for this date
        existing_log = DailyLog.objects.filter(
            user=request.user, 
            date=initial_date
        ).first()
        
        if existing_log:
            form = DailyLogForm(instance=existing_log)
        else:
            form = DailyLogForm(initial={'date': initial_date})
    
    return render(request, 'tracker/daily_log_form.html', {'form': form})

@login_required
def calendar_view(request, year=None, month=None):
    # Get current year and month if not provided
    if year is None or month is None:
        today = timezone.now().date()
        year = today.year
        month = today.month
    else:
        year = int(year)
        month = int(month)
    
    # Calculate previous and next month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Get month range
    _, num_days = monthrange(year, month)
    
    # Create calendar days
    calendar_days = []
    
    # Get daily logs for this month
    daily_logs = DailyLog.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )
    
    # Create a dictionary for quick lookup
    log_dict = {log.date.day: log for log in daily_logs}
    
    # Generate calendar
    for day in range(1, num_days + 1):
        date = datetime(year, month, day).date()
        log_entry = log_dict.get(day)
        
        calendar_days.append({
            'day': day,
            'date': date,
            'log': log_entry,
            'is_today': date == timezone.now().date()
        })
    
    context = {
        'year': year,
        'month': month,
        'month_name': datetime(year, month, 1).strftime('%B'),
        'calendar_days': calendar_days,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    
    return render(request, 'tracker/calendar.html', context)

@login_required
def statistics(request):
    cycles = Cycle.objects.filter(user=request.user)
    
    stats = {
        'total_cycles': cycles.count(),
        'avg_cycle_length': cycles.aggregate(Avg('cycle_length'))['cycle_length__avg'],
        'avg_period_length': cycles.aggregate(Avg('period_length'))['period_length__avg'],
    }
    
    symptoms = Symptom.objects.filter(user=request.user).values('symptom_type').annotate(
        count=Count('symptom_type')
    ).order_by('-count')
    
    moods = Mood.objects.filter(user=request.user).values('mood_type').annotate(
        count=Count('mood_type')
    ).order_by('-count')
    
    context = {
        'stats': stats,
        'symptoms': symptoms,
        'moods': moods,
        'cycles': cycles,
    }
    
    return render(request, 'tracker/statistics.html', context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        # Handle password change
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the error below.')
        # Handle profile update
        elif 'update_profile' in request.POST:
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings')
    else:
        password_form = PasswordChangeForm(request.user)
    
    # Get user statistics for display
    user_cycles = Cycle.objects.filter(user=request.user)
    total_cycles = user_cycles.count()
    total_symptoms = Symptom.objects.filter(user=request.user).count()
    total_moods = Mood.objects.filter(user=request.user).count()
    total_daily_logs = DailyLog.objects.filter(user=request.user).count()
    
    context = {
        'password_form': password_form,
        'total_cycles': total_cycles,
        'total_symptoms': total_symptoms,
        'total_moods': total_moods,
        'total_daily_logs': total_daily_logs,
    }
    
    return render(request, 'tracker/settings.html', context)
from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('login')