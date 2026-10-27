	
import json
import logging
import os

import requests
from dotenv import load_dotenv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request

load_dotenv()
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName") or data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName") or data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"},
                status=400
            )

        User.objects.create_user(username=username, password=password)

        return JsonResponse(
            {"userName": username, "status": "Registered"},
            status=201
        )

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def get_cars(request):
    cars = []

    for make in CarMake.objects.all():
        for model in make.car_models.all():
            cars.append({
                "Id": make.id,
                "Name": make.name,
                "DealerId": model.dealer_id,
                "Model": model.name,
                "Type": model.type,
                "Year": model.year
            })

    return JsonResponse(cars, safe=False)


def get_dealerships(request):
    state = request.GET.get("state")

    try:
        endpoint = (
            f"/fetchDealers/{state}" if state
            else "/fetchDealers"
        )
        response = get_request(endpoint)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)

    except requests.RequestException:
        logger.exception("Error fetching dealerships")
        return JsonResponse(
            {"error": "Unable to fetch dealerships"},
            status=502
        )


def get_dealer_details(request, dealer_id):
    try:
        response = get_request(f"/fetchDealer/{dealer_id}")
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)

    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            return JsonResponse(
                {"error": "Dealership not found"},
                status=404
            )

        logger.exception("Error fetching dealership details")
        return JsonResponse(
            {"error": "Unable to fetch dealership details"},
            status=502
        )

    except requests.RequestException:
        logger.exception("Error fetching dealership details")
        return JsonResponse(
            {"error": "Unable to fetch dealership details"},
            status=502
        )


def get_dealer_reviews(request, dealer_id):
    try:
        response = get_request(f"/fetchReviews/dealer/{dealer_id}")
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)

    except requests.RequestException:
        logger.exception("Error fetching dealer reviews")
        return JsonResponse(
            {"error": "Unable to fetch dealer reviews"},
            status=502
        )


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        backend_url = os.getenv(
            "backend_url", "http://localhost:3030"
        ).rstrip("/")

        response = requests.post(
            f"{backend_url}/insert_review",
            json=data,
            timeout=10
        )
        response.raise_for_status()

        return JsonResponse(response.json(), status=201)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except requests.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else 502
        )
        return JsonResponse(
            {"error": "Unable to submit review"},
            status=status_code
        )

    except requests.RequestException:
        logger.exception("Error submitting review")
        return JsonResponse(
            {"error": "Unable to submit review"},
            status=502
        )

import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"},
                status=400
            )

        User.objects.create_user(username=username, password=password)

        return JsonResponse(
            {"userName": username, "status": "Registered"},
            status=201
        )

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def get_cars(request):
    cars = []

    for make in CarMake.objects.all():
        models = make.car_models.all()

        for model in models:
            cars.append({
                "Id": make.id,
                "Name": make.name,
                "DealerId": model.dealer_id,
                "Model": model.name,
                "Type": model.type,
                "Year": model.year
            })

    return JsonResponse(cars, safe=False)











import json
import logging

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request
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
    return JsonResponse({
        "userName": "",
        "status": "Logged out"
    })

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


# Dealer reviews - implement in the reviews task


# Dealer details - implement in the dealership API task


# Add a dealer review - implement in the reviews task
