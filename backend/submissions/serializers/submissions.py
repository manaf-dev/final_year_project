from rest_framework import serializers

from accounts.models.users import UserAccount
from submissions.models.submissions import Submission, SubmissionVideo
from accounts.serializers.users import UserAccountSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class SubmissionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionVideo
        fields = "__all__"

    def validate(self, attrs):
        video_url = attrs.get("video_url")
        if video_url:
            validator = URLValidator()
            try:
                validator(video_url)
            except ValidationError:
                raise serializers.ValidationError({"video_url": "Enter a valid URL."})
        return attrs


class SubmissionSerializer(serializers.ModelSerializer):
    # intern = UserAccountSerializer(read_only=True)
    # intern_source = serializers.PrimaryKeyRelatedField(
    #     source="intern", queryset=UserAccount.objects.all(), write_only=True
    # )

    class Meta:
        model = Submission
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["intern"] = UserAccountSerializer(instance.intern).data

        # Add new grading data
        try:
            from submissions.selectors.grades import get_intern_grade_by_id

            intern_grades = get_intern_grade_by_id(instance.intern.id)

            if intern_grades:
                # Add current grade for this month from new grading system
                month_field_mapping = {
                    "1": "portfolio_month_1",
                    "2": "portfolio_month_2",
                    "3": "portfolio_month_3",
                    "4": "portfolio_month_4",
                }

                month_field = month_field_mapping.get(instance.month)
                if month_field:
                    current_grade = getattr(intern_grades, month_field, None)
                    data["current_grade"] = current_grade
                    data["is_graded_new_system"] = current_grade is not None

                    # For month 4, also include other components
                    if instance.month == "4":
                        data["teaching_philosophy_score"] = (
                            intern_grades.teaching_philosophy_score
                        )
                        data["reflective_practice_score"] = (
                            intern_grades.reflective_practice_score
                        )
                        # Calculate total for month 4
                        portfolio_score = current_grade or 0
                        philosophy_score = intern_grades.teaching_philosophy_score or 0
                        reflective_score = intern_grades.reflective_practice_score or 0
                        data["month_4_total"] = (
                            portfolio_score + philosophy_score + reflective_score
                        )
                else:
                    data["current_grade"] = None
                    data["is_graded_new_system"] = False
            else:
                data["current_grade"] = None
                data["is_graded_new_system"] = False

        except Exception as e:
            # Fallback to old system
            data["current_grade"] = instance.grade
            data["is_graded_new_system"] = False

        try:
            if instance.video:
                data["video"] = SubmissionVideoSerializer(instance.video).data
        except:
            return data

        return data
