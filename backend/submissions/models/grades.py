import uuid
from django.db import models
from accounts.models.users import UserAccount


class InternGrade(models.Model):
    """
    New grading model to handle the three components:
    - Portfolio (images/videos from months 1-4): 100 points (20+20+20+40)
    - Teaching Philosophy: 100 points
    - Reflective Practice: 100 points
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intern = models.OneToOneField(
        UserAccount, related_name="grades", on_delete=models.CASCADE
    )

    # Portfolio components (images/videos from months 1-4)
    portfolio_month_1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 20",
    )
    portfolio_month_2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 20",
    )
    portfolio_month_3 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 20",
    )
    portfolio_month_4 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 40",
    )

    # Document components
    teaching_philosophy_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 100",
    )
    reflective_practice_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Score out of 100",
    )

    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    graded_by = models.ForeignKey(
        UserAccount,
        related_name="graded_interns",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "submissions_intern_grade"

    def __str__(self):
        return f"Grades for {self.intern.username}"

    @property
    def portfolio_total(self):
        """Calculate total portfolio score out of 100"""
        scores = [
            self.portfolio_month_1 or 0,
            self.portfolio_month_2 or 0,
            self.portfolio_month_3 or 0,
            self.portfolio_month_4 or 0,
        ]
        return sum(scores)

    @property
    def overall_total(self):
        """Calculate total score out of 300"""
        portfolio = self.portfolio_total
        philosophy = self.teaching_philosophy_score or 0
        reflective = self.reflective_practice_score or 0
        return portfolio + philosophy + reflective

    @property
    def is_portfolio_complete(self):
        """Check if all portfolio components are graded"""
        return all(
            [
                self.portfolio_month_1 is not None,
                self.portfolio_month_2 is not None,
                self.portfolio_month_3 is not None,
                self.portfolio_month_4 is not None,
            ]
        )

    @property
    def is_fully_graded(self):
        """Check if all components are graded"""
        return (
            self.is_portfolio_complete
            and self.teaching_philosophy_score is not None
            and self.reflective_practice_score is not None
        )
