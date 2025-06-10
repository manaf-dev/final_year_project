from ._base_imports import *

from submissions.models.notifications import Notification
from submissions.serializers.notifications import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_notifications(self, request):
        user = request.user
        if not user:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        notifications = self.queryset.filter(receiver=user).order_by("-timestamp")
        if not notifications:
            return Response([], status=status.HTTP_200_OK)

        notifications_data = self.get_serializer(notifications, many=True).data
        return Response(notifications_data, status=status.HTTP_200_OK)

    def mark_as_read(self, request, notification_id):
        notification = self.queryset.get(id=notification_id)
        if not notification:
            return Response(
                {"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
            )
        notification.read = True
        notification.save()
        return Response(
            {"detail": "Notification marked as read"}, status=status.HTTP_200_OK
        )

    def mark_all_as_read(self, request):
        notifications = self.queryset.filter(read=False)
        if not notifications:
            return Response(
                {"detail": "No unread notifications"},
                status=status.HTTP_208_ALREADY_REPORTED,
            )
        notifications.update(read=True)
        return Response(
            {"detail": "Notifications marked as read"}, status=status.HTTP_200_OK
        )

    def get_unread_count(self, request):
        user = request.user
        if not user:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        unread_count = self.queryset.filter(receiver=user, read=False).count()
        return Response({"unread_count": unread_count}, status=status.HTTP_200_OK)
