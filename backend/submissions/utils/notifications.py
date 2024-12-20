from submissions.models.notifications import Notification


def create_notification(receiver, title, content):
    notification = Notification.objects.create(
        receiver=receiver, title=title, content=content
    )
    return notification
