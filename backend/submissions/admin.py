from django.contrib import admin

from submissions.models.submissions import Submission, SubmissionVideo, Comment
from submissions.models.portfolios import PortfolioImage, PortfolioFile
from submissions.models.notifications import Notification
from submissions.models.grades import InternGrade

admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioFile)
admin.site.register(Notification)
admin.site.register(SubmissionVideo)
admin.site.register(InternGrade)
