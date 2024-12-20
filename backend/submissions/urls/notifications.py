from django.urls import path

from submissions.views.notifications import NotificationViewSet

NOTIFICATION_URLS = [
    path("notifications/", NotificationViewSet.as_view({"get": "get_notifications"})),
]
