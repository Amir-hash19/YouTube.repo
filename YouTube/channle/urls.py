from django.urls import path
from .views import CreateChannelView, SubscribeChannelView, UnsubscribeChannelView, EditChannelView


urlpatterns = [
    path("build/", CreateChannelView.as_view(), name="create-channel"),
    path("subscribtion/subscribe/", SubscribeChannelView.as_view(), name="user-subscribe"),
    path("subscribtion/unsubscribe/", UnsubscribeChannelView.as_view(), name="user-unsubscribe"),
    path("channel/slug:slug/", EditChannelView.as_view(), name="edit-channel")
]
