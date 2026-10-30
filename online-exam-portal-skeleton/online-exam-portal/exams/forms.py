"""Forms for the exams app. Owner: Thejas."""
from django import forms

from .models import Exam


class ExamForm(forms.ModelForm):
    """Create / edit an examination. Model.clean() holds the cross-field rules."""

    class Meta:
        model = Exam
        fields = ["title", "description", "duration_minutes", "start_time", "end_time"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }
        labels = {"duration_minutes": "Duration (minutes)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("start_time", "end_time"):
            self.fields[name].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        self.fields["duration_minutes"].min_value = 1
        self.fields["duration_minutes"].widget.attrs["min"] = 1

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if not description:
            raise forms.ValidationError("Description is required.")
        return description
