from rest_framework import serializers
from submissions.models.grades import InternGrade
from accounts.serializers.users import UserAccountSerializer


class InternGradeSerializer(serializers.ModelSerializer):
    intern = UserAccountSerializer(read_only=True)
    graded_by = UserAccountSerializer(read_only=True)
    portfolio_total = serializers.ReadOnlyField()
    overall_total = serializers.ReadOnlyField()
    is_portfolio_complete = serializers.ReadOnlyField()
    is_fully_graded = serializers.ReadOnlyField()

    class Meta:
        model = InternGrade
        fields = [
            "id",
            "intern",
            "portfolio_month_1",
            "portfolio_month_2",
            "portfolio_month_3",
            "portfolio_month_4",
            "teaching_philosophy_score",
            "reflective_practice_score",
            "portfolio_total",
            "overall_total",
            "is_portfolio_complete",
            "is_fully_graded",
            "created_at",
            "updated_at",
            "graded_by",
        ]

    # def to_


class UpdatePortfolioScoreSerializer(serializers.Serializer):
    intern_id = serializers.UUIDField()
    month = serializers.IntegerField(min_value=1, max_value=4)
    score = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0)

    def validate_score(self, value):
        month = self.initial_data.get("month")
        if month in [1, 2, 3] and value > 20:
            raise serializers.ValidationError(
                "Score for months 1-3 cannot exceed 20 points"
            )
        elif month == 4 and value > 40:
            raise serializers.ValidationError(
                "Score for month 4 cannot exceed 40 points"
            )
        return value


class UpdateTeachingPhilosophyScoreSerializer(serializers.Serializer):
    intern_id = serializers.UUIDField()
    score = serializers.DecimalField(
        max_digits=5, decimal_places=2, min_value=0, max_value=100
    )


class UpdateReflectivePracticeScoreSerializer(serializers.Serializer):
    intern_id = serializers.UUIDField()
    score = serializers.DecimalField(
        max_digits=5, decimal_places=2, min_value=0, max_value=100
    )
