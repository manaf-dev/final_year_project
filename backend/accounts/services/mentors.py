from accounts.models.mentors import Mentor


def create_mentor(mentor: dict):
    try:
        mentor = Mentor.objects.create(
            name=mentor["name"], phone=mentor["phone"], email=mentor.get("email")
        )
        return mentor
    except:
        return None
