from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import( CreateChannelView, SubscribeChannelView, UnsubscribeChannelView,
EditChannelView, DeleteChannelView, DetailChannelView, ChannelViewSet, ChannelSubsVeiwSet)


router = DefaultRouter()
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'subchannel', ChannelSubsVeiwSet, basename='subchannel')

urlpatterns = [
    path("build/", CreateChannelView.as_view(), name="create-channel"),
    path("subscribtion/subscribe/", SubscribeChannelView.as_view(), name="user-subscribe"),
    path("subscribtion/unsubscribe/", UnsubscribeChannelView.as_view(), name="user-unsubscribe"),
    path("channel/slug:slug/", EditChannelView.as_view(), name="edit-channel"),
    path("channels/delete/<str:channel_id>/", DeleteChannelView.as_view(), name="delete-channel"),
    path("channel/view/", DetailChannelView.as_view(), name="detail-channel"),
    path('api/', include(router.urls)),

]

