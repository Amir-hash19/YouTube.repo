from django.urls import path
from .views import CreateChannelView


urlpatterns = [
    path("Channel/create/", CreateChannelView.as_view(), name="create-channel")
]
