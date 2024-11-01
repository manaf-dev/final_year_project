from accounts.models.intern_schools import InternSchool


def create_school(school: dict):
    print("School in service:", school)
    try:
        school = InternSchool.objects.create(
            name=school["name"],
            address=school["address"],
            location=school["location"],
            district=school["district"],
            region=school["region"],
        )
        return school
    except:
        return None
