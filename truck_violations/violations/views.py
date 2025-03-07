from django.shortcuts import render, redirect
from .forms import ViolatorForm, ViolationRecordForm


def violator_view(request):
    if request.method == 'POST':
        # Έλεγχος ποια φόρμα υποβλήθηκε
        if 'violator_submit' in request.POST:
            violator_form = ViolatorForm(request.POST)
            if violator_form.is_valid():
                violator_form.save()
                return redirect('success_url')  # Αντικατέστησε με το URL της επιτυχίας
        elif 'violation_record_submit' in request.POST:
            violation_record_form = ViolationRecordForm(request.POST)
            if violation_record_form.is_valid():
                violation_record_form.save()
                return redirect('success_url')  # Αντικατέστησε με το URL της επιτυχίας
    else:
        violator_form = ViolatorForm()
        violation_record_form = ViolationRecordForm()

    context = {
        'violator_form': violator_form,
        'violation_record_form': violation_record_form,
    }
    return render(request, 'violator_form.html', context)