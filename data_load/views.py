import csv

from django.shortcuts import render

from data_load.forms import UploadFileForm
from data_load.management.commands.import_css_calls import process_csv as process_css_calls_csv
from data_load.management.commands.import_css_cases import process_csv as process_css_cases_csv
from data_load.management.commands.import_rms_cases import process_csv as process_rms_cases_csv
# from data_load.management.commands.import_css_calls import process_csv as process_css_call_csv

def import_csv(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['file_type']
            if file_type == 'CSS calls':
                process_css_calls_csv(form.cleaned_data['file'], True)
            elif file_type == 'CSS cases':
                process_css_cases_csv(form.cleaned_data['file'], True)
            elif file_type == 'RMS cases':
                process_rms_cases_csv(form.cleaned_data['file'], True, True)

        else:
            print form.errors
            print request.FILES
    else:
        form = UploadFileForm()

    return render(request, 'data_load/import_csv.html', {'form': form})
