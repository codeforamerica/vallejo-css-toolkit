from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect

from workflow.models import CSSCall


@login_required(login_url='/admin/login/')
def landing(request):

    # TODO: do a proper filter
    newest_calls = CSSCall.objects.filter()[:5].values_list('date', 'name', 'address', 'problem', 'id')

    # TODO: fetch this from the case audit log when it's implemented
    recent_activities = [
        'Tina Encarnacion contacted the owner of 2 Florida Street.',
        'Lt. Park closed a case at 555 Santa Clara Street.',
        'Cpl. Garcia conducted a site visit at 111 Amador Street.'
    ]

    return render(
        request,
        'workflow/landing.html',
        {
            'newest_calls': newest_calls,
            'recent_activities': recent_activities,
            'new_report_count': 17
        }
    )


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out.")
    return HttpResponseRedirect('/login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.WARNING, "This user account is disabled.")
        else:
            messages.add_message(request, messages.WARNING, "The user nane or password is incorrect.")
    else:
        users = User.objects.filter(id=request.user.id)
        user = users and users[0]
        if user and user.is_authenticated:
            return HttpResponseRedirect('/')

    return render(request, 'workflow/login.html', {'exclude_navbar': True})
