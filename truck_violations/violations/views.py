from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Violator, ViolationRecord
from .forms import ViolationRecordForm
from datetime import datetime


class ViolationRecordView(View):
    template_name = 'record_violation.html'
    form_class = ViolationRecordForm

    def get(self, request):
        context = {
            'form': self.form_class(),
            'violations_records': None,
            'total_fine': 0,
            'success_message': None
        }

        if 'circulation_number' in request.GET:
            circulation_number = request.GET.get('circulation_number')
            context.update(self.get_violator_data(circulation_number))

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {
            'form': form,
            'violations_records': None,
            'total_fine': 0,
            'success_message': None
        }

        if form.is_valid():
            violator = self.get_or_create_violator(form)
            self.create_violation_record(form, violator)

            # Ανάκτηση δεδομένων παραβάτη μετά την καταχώρηση
            violator_data = self.get_violator_data(violator.circulation_number)
            context.update(violator_data)
            context['success_message'] = 'Η παράβαση καταχωρήθηκε επιτυχώς.'

        return render(request, self.template_name, context)

    def get_violator_data(self, circulation_number):
        result = {
            'violations_records': None,
            'total_fine': 0,
            'violator_name': ''
        }

        try:
            violator = Violator.objects.get(circulation_number=circulation_number)
            result['violator_name'] = violator.name

            violations_records = ViolationRecord.objects.filter(
                violator=violator
            ).order_by('-datetime_inspection')

            result['violations_records'] = violations_records
            result['total_fine'] = self.calculate_total_fine(violations_records)

            # Προσυμπλήρωση φόρμας με τα στοιχεία του παραβάτη
            result['form'] = self.form_class(initial={
                'circulation_number': circulation_number,
                'name': violator.name
            })
        except Violator.DoesNotExist:
            # Αν δεν υπάρχει παραβάτης, προσυμπληρώνουμε μόνο τον αριθμό κυκλοφορίας
            result['form'] = self.form_class(initial={
                'circulation_number': circulation_number
            })

        return result

    def get_or_create_violator(self, form):
        circulation_number = form.cleaned_data['circulation_number']
        name = form.cleaned_data['name']

        violator, created = Violator.objects.get_or_create(
            circulation_number=circulation_number,
            defaults={'name': name}
        )

        # Αν ο παραβάτης υπάρχει αλλά το όνομα είναι διαφορετικό, ενημερώνουμε το όνομα
        if not created and violator.name != name:
            violator.name = name
            violator.save()

        return violator

    def create_violation_record(self, form, violator):
        return ViolationRecord.objects.create(
            violator=violator,
            violation=form.cleaned_data['violation'],
            datetime_inspection=form.cleaned_data['datetime_inspection'],
            previous_inspection=form.cleaned_data['previous_inspection'],
            kind_violator=form.cleaned_data['kind_violator']
        )

    @staticmethod
    def calculate_total_fine(violations_records):
        """
        Υπολογίζει το συνολικό πρόστιμο σύμφωνα με τον κανόνα:
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


class CalculateDaysDifferenceView(View):
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Έλεγχος ότι είναι AJAX request
            try:
                previous_date = request.GET.get('previous_date')
                current_date = request.GET.get('current_date')

                if not previous_date or not current_date:
                    return JsonResponse({'error': 'Missing date parameters'}, status=400)

                previous_date = datetime.strptime(previous_date, '%Y-%m-%dT%H:%M')
                current_date = datetime.strptime(current_date, '%Y-%m-%dT%H:%M')

                if previous_date > current_date:
                    return JsonResponse({'error': 'Η προηγούμενη ημερομηνία δεν μπορεί να είναι '
                                                  'μεγαλύτερη από την τρέχουσα!'}, status=400)

                days_difference = (current_date - previous_date).days

                return JsonResponse({'days_difference': days_difference})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'error': 'Invalid request'}, status=400)
