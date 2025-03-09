from django import forms
from .models import Violator, ViolationRecord, Violation
from datetime import datetime


class ViolationRecordForm(forms.Form):
    circulation_number = forms.CharField(
        max_length=20,
        label='ΑΡΙΘΜΟΣ ΚΥΚΛΟΦΟΡΙΑΣ',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=50,
        label='ΟΝΟΜΑΤΕΠΩΝΥΜΟ',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    previous_inspection = forms.DateTimeField(
        label='ΗΜΕΡΟΜΗΝΙΑ ΠΡΟΗΓΟΥΜΕΝΟΥ ΕΛΕΓΧΟΥ',
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    datetime_inspection = forms.DateTimeField(
        label='ΗΜΕΡΟΜΗΝΙΑ ΚΑΙ ΩΡΑ ΕΛΕΓΧΟΥ',
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        initial=datetime.now
    )
    kind_violator = forms.ChoiceField(
        choices=ViolationRecord.VIOLATOR_CHOICES,
        label='ΙΔΙΟΚΤΗΤΗΣ / ΟΔΗΓΟΣ',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    violation = forms.ModelChoiceField(
        queryset=Violation.objects.filter(is_active=True),
        label='ΑΡΙΘΜΟΣ ΠΑΡΑΒΑΣΗΣ',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        previous_inspection = cleaned_data.get('previous_inspection')
        datetime_inspection = cleaned_data.get('datetime_inspection')

        if previous_inspection and datetime_inspection and previous_inspection > datetime_inspection:
            raise forms.ValidationError(
                "Η ημερομηνία προηγούμενου ελέγχου δεν μπορεί να είναι μεταγενέστερη της τρέχουσας ημερομηνίας ελέγχου.")

        return cleaned_data
