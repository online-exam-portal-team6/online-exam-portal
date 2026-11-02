
"""Forms for the questions app. Owner: Thejas."""

from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):
    """Form for creating an MCQ question (OEP-F-011)."""

    class Meta:
        model = Question
        fields = [
            "text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
        ]
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Enter your question here...",
            }),
            "option_a": forms.TextInput(attrs={
                "placeholder": "Enter option A",
            }),
            "option_b": forms.TextInput(attrs={
                "placeholder": "Enter option B",
            }),
            "option_c": forms.TextInput(attrs={
                "placeholder": "Enter option C",
            }),
            "option_d": forms.TextInput(attrs={
                "placeholder": "Enter option D",
            }),
        }
        labels = {
            "text": "Question",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_option": "Correct answer",
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()

        if not text:
            raise forms.ValidationError("Question text cannot be empty.")

        return text

    def clean(self):
        cleaned_data = super().clean()

        option_fields = [
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        ]

        for field in option_fields:
            value = cleaned_data.get(field)

            if value and not value.strip():
                self.add_error(field, "This option cannot be empty.")
            elif value:
                cleaned_data[field] = value.strip()

        return cleaned_data
