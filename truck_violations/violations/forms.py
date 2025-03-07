from django import forms
from .models import Violator, ViolationRecord, Violation
from datetime import datetime


class ViolatorForm(forms.ModelForm):
    class Meta:
        model = Violator
        fields = ['circulation_number', 'name']
        labels = {
            'circulation_number': 'Αριθμός Κυκλοφορίας',
            'name': 'Ονοματεπώνυμο'
        }


class ViolationRecordForm(forms.ModelForm):
    previous_inspection_date = forms.DateField(
        label='Προηγούμενη Ημερομηνία Ελέγχου',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )
    days_passed = forms.IntegerField(
        label='Διαφορά σε Ημέρες',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False,
    )

    class Meta:
        model = ViolationRecord
        fields = ['violation', 'datetime_inspection', 'kind_violator']
        labels = {
            'violation': 'Αριθμός Παράβασης',
            'datetime_inspection': 'Ημερομηνία και Ώρα Ελέγχου',
            'kind_violator': 'Τύπος Παραβάτη',
        }
        widgets = {
            'datetime_inspection': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datetime_inspection'].widget.attrs.update({'onchange': 'calculateDays()'})
        self.fields['previous_inspection_date'].widget.attrs.update({'onchange': 'calculateDays()'})

    def clean(self):
        cleaned_data = super().clean()
        previous_inspection_date = cleaned_data.get('previous_inspection_date')
        current_inspection_date = cleaned_data.get('datetime_inspection')

        if previous_inspection_date and current_inspection_date:
            if previous_inspection_date > current_inspection_date:
                raise forms.ValidationError(
                    "Η προηγούμενη ημερομηνία δεν μπορεί να είναι μετά την τρέχουσα ημερομηνία ελέγχου.")

            delta = current_inspection_date - previous_inspection_date
            cleaned_data['days_passed'] = delta.days

        return cleaned_data
