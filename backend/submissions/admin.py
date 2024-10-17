from django.contrib import admin

from submissions.models import *

admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioFile)
