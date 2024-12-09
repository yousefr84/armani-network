from django import forms
from .models import Mentor, Services


class MentorAdminForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Services.objects.all(),

    )

    class Meta:
        model = Mentor
        fields = '__all__'
