from django.urls import path
from .views import CreateChannelView


urlpatterns = [
    path("build/", CreateChannelView.as_view(), name="create-channel")
]
