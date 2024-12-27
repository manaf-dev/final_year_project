from ._base_imports import *

from accounts.serializers.intern_schools import InternSchoolSerializer
from accounts.models.intern_schools import InternSchool
from accounts.serializers.users import CustomUserSerializer


class InternSchoolViewSet(viewsets.ModelViewSet):
    queryset = InternSchool.objects.all()
    serializer_class = InternSchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create_school(self, request):
        school = request.data
        intern = request.user

        if not intern:
            context = {
                "detail": "You can't perform this operation",
            }
            raise NotFound(context)
        elif intern.intern_school:
            context = {
                "detail": "You have a school already.",
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = self.get_serializer(data=school)
        serializer.is_valid(raise_exception=True)
        created_school = serializer.save()

        if created_school:
            intern.intern_school = created_school
            intern.save()
            user_serializer = CustomUserSerializer(intern)
            context = {
                "user": user_serializer.data,
                "detail": "Internship school added successful",
            }
            return Response(
                context,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "Could not create school"}, status=status.HTTP_400_BAD_REQUEST
        )
