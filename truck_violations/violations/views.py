from django.shortcuts import render
from django.http import JsonResponse
from .models import Violator, ViolationRecord, Violation
from .forms import ViolationRecordForm
from datetime import datetime


def record_violation(request):
    if request.method == 'POST':
        form = ViolationRecordForm(request.POST)
        if form.is_valid():
            circulation_number = form.cleaned_data['circulation_number']
            name = form.cleaned_data['name']
            previous_inspection = form.cleaned_data['previous_inspection']
            datetime_inspection = form.cleaned_data['datetime_inspection']
            kind_violator = form.cleaned_data['kind_violator']
            violation = form.cleaned_data['violation']

            # Αναζήτηση ή δημιουργία Violator
            violator, created = Violator.objects.get_or_create(
                circulation_number=circulation_number,
                defaults={'name': name}
            )

            # Αν ο παραβάτης υπάρχει αλλά το όνομα είναι διαφορετικό, ενημερώνουμε το όνομα
            if not created and violator.name != name:
                violator.name = name
                violator.save()

            # Δημιουργία της εγγραφής παράβασης
            violation_record = ViolationRecord.objects.create(
                violator=violator,
                violation=violation,
                datetime_inspection=datetime_inspection,
                previous_inspection=previous_inspection,
                kind_violator=kind_violator
            )

            # Ανάκτηση όλων των παραβάσεων για αυτόν τον παραβάτη
            violations_records = ViolationRecord.objects.filter(violator=violator).order_by('-datetime_inspection')

            # Υπολογισμός συνολικού προστίμου
            total_fine = calculate_total_fine(violations_records)

            return render(request, 'record_violation.html', {
                'form': ViolationRecordForm(),
                'violations_records': violations_records,
                'total_fine': total_fine,
                'success_message': 'Η παράβαση καταχωρήθηκε επιτυχώς.'
            })
    else:
        form = ViolationRecordForm()

    return render(request, 'record_violation.html', {'form': form})


def calculate_days_difference(request):
    """AJAX view για υπολογισμό διαφοράς ημερών"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            previous_date = request.POST.get('previous_date')
            current_date = request.POST.get('current_date')

            if not previous_date:
                return JsonResponse({'days_difference': '-'})

            previous_date = datetime.strptime(previous_date, '%Y-%m-%dT%H:%M')
            current_date = datetime.strptime(current_date, '%Y-%m-%dT%H:%M')

            days_difference = (current_date - previous_date).days

            return JsonResponse({'days_difference': days_difference})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def calculate_total_fine(violations_records):
    """
    Υπολογίζει το συνολικό πρόστιμο σύμφωνα με τον κανόνα:
    - Κρατάμε το μεγαλύτερο πρόστιμο
    - Προσθέτουμε τα υπόλοιπα * 10%
    """
    if not violations_records:
        return 0

    fines = []
    for record in violations_records:
        if record.kind_violator == ViolationRecord.DRIVER:
            fine = record.violation.driver_fine
        else:
            fine = record.violation.owner_fine

        if fine:
            fines.append(float(fine))

    if not fines:
        return 0

    # Βρίσκουμε το μεγαλύτερο πρόστιμο
    max_fine = max(fines)

    # Υπολογίζουμε το 10% των υπόλοιπων προστίμων
    other_fines_sum = sum([f for f in fines if f != max_fine])
    other_fines_10_percent = other_fines_sum * 0.1

    # Συνολικό πρόστιμο
    total_fine = max_fine + other_fines_10_percent

    return round(total_fine, 2)