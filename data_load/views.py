import csv

from django.shortcuts import render

from data_load.forms import UploadFileForm
from data_load.management.commands.import_css_calls import process_csv

def import_css_calls(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_csv(form.cleaned_data['file'], True)
        else:
            print form.errors
            print request.FILES
    else:
        form = UploadFileForm()

    return render(request, 'data_load/import_css_calls.html', {'form': form})
