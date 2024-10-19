from django.urls import path

from accounts.views import portfolios

PORTFOLIOS_URLS = [path("portfolios/", portfolios.portfolios, name="")]
