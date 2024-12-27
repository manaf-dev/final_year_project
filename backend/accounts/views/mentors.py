from ._base_imports import *

from accounts.models.mentors import Mentor
from accounts.serializers.mentors import MentorSerializer
from accounts.selectors.users import get_user_by_id
from accounts.services.mentors import create_mentor


class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def create_mentor(self, request):
        mentor = request.data
        user = request.user
        intern = get_user_by_id(user.id)

        if not intern:
            context = {
                "detail": "You can't perform this operation",
            }
            raise NotFound(context)
        elif intern.mentor:
            context = {
                "detail": "You have a mentor already.",
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = self.get_serializer(data=mentor)
        serializer.is_valid(raise_exception=True)
        created_mentor = serializer.save()

        if created_mentor:
            intern.mentor = created_mentor
            intern.save()
            return Response(
                {"detail": "Mentor Details Saved"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail": "Could not create mentor"}, status=status.HTTP_403_FORBIDDEN
            )
