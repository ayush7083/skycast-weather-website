from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .utils import get_weather_data
from .models import SearchHistory
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
def weather_api(request):
    city = request.GET.get('city')
    if not city:
        return Response({"success": False, "error": "City parameter is required."}, status=400)

    # Clean the city name (remove anything in parentheses)
    city = city.split('(')[0].strip()

    data = get_weather_data(city)

    # Save to history if user is authenticated and fetch was successful
    if request.user.is_authenticated and data.get("success"):
        SearchHistory.objects.create(user=request.user, city=city)

    return Response(data)


@login_required
def home(request):
    # Fetch the 5 most recent searches by this user
    history = SearchHistory.objects.filter(user=request.user).order_by('-searched_at')[:5]
    return render(request, "weather/home.html", {"history": history})
