
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('registration', views.registration, name='registration'),
    path('get_cars', views.get_cars, name='get_cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("registration", views.registration, name="registration"),
    path("get_cars", views.get_cars, name="get_cars"),

    path("get_dealerships", views.get_dealerships, name="get_dealerships"),
    path("get_dealerships/<str:state>", views.get_dealerships, name="get_dealerships_by_state"),
    path("get_dealer_details/<int:dealer_id>", views.get_dealer_details, name="get_dealer_details"),
    path("get_dealer_reviews/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews"),
    path("add_review", views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
