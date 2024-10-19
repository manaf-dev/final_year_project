from . import departments, intern_schools, portfolios, users


URL_COMPONENTS = (
    departments.DEPARTMENTS_URLS
    + intern_schools.INTERN_SCHOOLS_URLS
    + portfolios.PORTFOLIOS_URLS
    + users.USERS_URLS
)

app_name = "accounts"

urlpatterns = URL_COMPONENTS
