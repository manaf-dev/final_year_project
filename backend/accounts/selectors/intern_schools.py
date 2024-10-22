from accounts.models.intern_schools import InternSchool


def get_intern_schools():
    return InternSchool.objects.all()


def get_intern_school_by_id(intern_school_id: int):
    try:
        intern_school = InternSchool.objects.get(id=intern_school_id)
    except InternSchool.DoesNotExist:
        return None
    else:
        return intern_school
