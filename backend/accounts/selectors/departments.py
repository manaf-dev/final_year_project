from accounts.models.departments import Department


def get_departments():
    return Department.objects.all()


def get_departments_by_id(department_id: int):
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return None
    else:
        return department
