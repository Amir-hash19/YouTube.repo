from django.urls import path
from .views import ListAdvertiserView, AdDetailView



urlpatterns = [
    path("Ad/list/", ListAdvertiserView.as_view(), name="list-advertisers"),
    path("Ad/detail/slug:slug/", AdDetailView.as_view(), name="detail-ad")
]
