from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models.users import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class BulkAssignmentForm(forms.Form):
    supervisor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(account_type="supervisor"),
        label="Select Supervisor",
        required=True,
    )
