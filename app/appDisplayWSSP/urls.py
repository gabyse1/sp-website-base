from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_page, name="get_page"),
    path("<str:lang>/<str:pagename>", views.get_page, name="get_page"),
    
    # API Routes
    path("retrieve/countries", views.retrieve_countries, name="retrieve_countries"),
]