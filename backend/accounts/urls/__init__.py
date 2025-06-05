from . import departments, users


URL_COMPONENTS = departments.DEPARTMENTS_URLS + users.USERS_URLS

app_name = "accounts"

urlpatterns = URL_COMPONENTS
