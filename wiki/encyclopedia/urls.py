from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.encyclopedia_entry, name="encyclopedia_entry"),
    #it works with slash to pass the query but without it doesn't work....
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/<str:title>/", views.editpage, name="editpage"),
    path("randompage/", views.randompage, name="randompage")
]
