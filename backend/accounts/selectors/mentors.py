from accounts.models.mentors import Mentor


def get_mentors():
    return Mentor.objects.all()


def get_mentor_by_id(mentor_id: int):
    try:
        mentor = Mentor.objects.get(id=mentor_id)
    except Mentor.DoesNotExist:
        return None
    else:
        return mentor
