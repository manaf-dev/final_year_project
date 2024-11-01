from ._base_imports import *

from accounts.serializers.intern_schools import InternSchoolSerializer
from accounts.models.intern_schools import InternSchool
from accounts.models.users import CustomUser
from accounts.selectors.users import get_user_by_id
from accounts.services.intern_schools import create_school


class InternSchoolViewSet(viewsets.ModelViewSet):
    queryset = InternSchool.objects.all()
    serializer_class = InternSchoolSerializer

    def new_intern_school(self, request):
        school = request.data
        user = request.user
        print(user)
        intern = get_user_by_id(user.id)

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
        created_school = create_school(serializer.data)

        if created_school:
            intern.intern_school = created_school
            intern.save()
            return Response(
                {"detail": "Internship School Details Saved"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Could not create school"}, status=status.HTTP_403_FORBIDDEN
            )
