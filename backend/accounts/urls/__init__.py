from . import departments, faculties, intern_schools, users


URL_COMPONENTS = (
    departments.DEPARTMENTS_URLS
    + faculties.FACULTIES_URLS
    + intern_schools.INTERN_SCHOOLS_URLS
    + users.USERS_URLS
)

app_name = "accounts"

urlpatterns = URL_COMPONENTS
