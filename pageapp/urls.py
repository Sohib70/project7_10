from .views import ListCreateApi,DetailUpdateDeleteApi
from django.urls import path

urlpatterns = [
    path("",ListCreateApi.as_view(),name="listcraete"),
    path("u/<int:pk>/",DetailUpdateDeleteApi.as_view())
]