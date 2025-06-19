from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from weather import views as weather_views  # ✅ For home & API route
from django.http import JsonResponse  # ✅ New import

# ✅ Health check view function
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Root URL redirects to home or register based on auth
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('register'), name='root_redirect'),

    # Home page for authenticated users
    path('home/', weather_views.home, name='home'),

    # Weather API
    path('api/weather/', weather_views.weather_api, name='weather_api'),

    # Weather app routes
    path('weather/', include('weather.urls')),

    # Authentication routes
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', accounts_views.register, name='register'),

    # ✅ Health check endpoint for Render
    path('healthz/', health_check),
]
