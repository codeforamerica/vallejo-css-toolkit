from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def property(request):

    return render(request, 'workflow/property.html')


@login_required(login_url='/login/')
def properties(request):

    return render(request, 'workflow/properties.html')
