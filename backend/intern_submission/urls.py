"""
URL configuration for intern_submission project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/submissions/", include("submissions.urls")),
    path("api/internships/", include("internships.urls")),
    # path("api-auth/", include("rest_framework.urls")),
    # path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    # path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    # path(
    #     "api/dj-rest-auth/verify-email/",
    #     VerifyEmailView.as_view(),
    #     name="rest_verify_email",
    # ),
    # path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    # path(
    #     "api/dj-rest-auth/account-confirm-email/",
    #     VerifyEmailView.as_view(),
    #     name="account_email_verification_sent",
    # ),
    # re_path(
    #     r"^account-confirm-email/(?P<key>[-:\w]+)/$",
    #     VerifyEmailView.as_view(),
    #     name="account_confirm_email",
    # ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
