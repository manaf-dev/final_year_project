from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models.users import UserAccount


class UserAccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserAccount
        fields = UserCreationForm.Meta.fields


class UserAccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = UserAccount
        fields = UserChangeForm.Meta.fields


class BulkAssignmentForm(forms.Form):
    supervisor = forms.ModelChoiceField(
        queryset=UserAccount.objects.filter(account_type="supervisor"),
        label="Select Supervisor",
        required=True,
    )
