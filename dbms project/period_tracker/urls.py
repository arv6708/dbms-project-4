from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    # Redirect accounts/ to our custom login
    path('accounts/login/', RedirectView.as_view(pattern_name='login')),
    path('accounts/logout/', RedirectView.as_view(pattern_name='logout')),
]