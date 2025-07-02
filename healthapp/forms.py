from django import forms
from .models import MentalHealthSubmission


SYMPTOM_CHOICES = [
    ('Anxiety', 'Anxiety'),
    ('Depression', 'Depression'),
    ('Stress', 'Stress'),
    ('Sleep Issues', 'Sleep Issues'),
    ('Mood Swings', 'Mood Swings'),
    ('Lack of Motivation', 'Lack of Motivation'),
]

class MentalHealthSurveyForm(forms.ModelForm):
    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = MentalHealthSubmission
        fields = ['name', 'email', 'stress_level', 'diagnosed', 'symptoms', 'other_issues']
