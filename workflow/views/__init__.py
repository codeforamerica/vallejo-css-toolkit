from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
