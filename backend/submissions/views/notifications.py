from ._base_imports import *

from submissions.models.notifications import Notification
from submissions.serializers.notifications import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_notifications(self, request):
        user = request.user
        notifications = self.queryset.filter(receiver=user)

        if not notifications:
            return Response({"detail": "No notifications"}, status=status.HTTP_200_OK)

        notifications_data = self.get_serializer(notifications, many=True).data
        return Response(notifications_data, status=status.HTTP_200_OK)
