from django.urls import path

from submissions.views.notifications import NotificationViewSet

NOTIFICATION_URLS = [
    path("notifications/", NotificationViewSet.as_view({"get": "get_notifications"})),
    path(
        "notifications/unread-count/",
        NotificationViewSet.as_view({"get": "get_unread_count"}),
    ),
    path(
        "notification/mark-as-read/<str:notification_id>/",
        NotificationViewSet.as_view({"put": "mark_as_read"}),
    ),
    path(
        "notification/delete/<str:pk>/",
        NotificationViewSet.as_view({"delete": "destroy"}),
    ),
    path(
        "notification/mark-all-as-read/",
        NotificationViewSet.as_view({"put": "mark_all_as_read"}),
    ),
]
