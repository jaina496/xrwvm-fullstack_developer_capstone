
import json
import logging

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)


# Login user
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:
        data = json.loads(request.body)
        username = data.get("userName", "").strip()
        password = data.get("password", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400
        )

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)
        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        })

    return JsonResponse({
        "userName": username,
        "status": "Invalid credentials"
    }, status=401)


# Logout user
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


# Register a new user
@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:
        data = json.loads(request.body)
        username = data.get("userName", "").strip()
        password = data.get("password", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Username already exists"},
            status=409
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    return JsonResponse({
        "userName": user.username,
        "status": "Registered"
    }, status=201)


# Get all car makes and associated models
def get_cars(request):
    car_makes = CarMake.objects.all().prefetch_related("car_models")
    cars = []

    for make in car_makes:
        car_models = []

        for model in make.car_models.all():
            car_models.append({
                "Id": model.id,
                "Name": model.name,
                "DealerId": model.dealer_id,
                "Type": model.type,
                "Year": model.year,
            })

        cars.append({
            "CarMake": make.name,
            "CarMakeId": make.id,
            "CarModels": car_models,
        })

    return JsonResponse(cars, safe=False)


# Dealership listing - implement in the dealership API task
def get_dealerships(request):
    return JsonResponse(
        {"error": "Dealership listing not implemented yet"},
        status=501
    )


# Dealer reviews - implement in the reviews task
def get_dealer_reviews(request, dealer_id):
    return JsonResponse(
        {"error": "Dealer reviews not implemented yet"},
        status=501
    )


# Dealer details - implement in the dealership API task
def get_dealer_details(request, dealer_id):
    return JsonResponse(
        {"error": "Dealer details not implemented yet"},
        status=501
    )


# Add a dealer review - implement in the reviews task
@csrf_exempt
def add_review(request):
    return JsonResponse(
        {"error": "Review submission not implemented yet"},
        status=501
    )
