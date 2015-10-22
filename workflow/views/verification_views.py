import logging
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from workflow.models import Verification

from workflow.forms import VerificationDetailsForm, VerificationOwnerForm

log = logging.getLogger('consolelogger')


@login_required(login_url='/admin/login/')
def verfication(request, verfication_id):
    instance = get_object_or_404(Verification, id=verfication_id)

    case_details_form = VerificationDetailsForm(request.POST or None, instance=instance)

    contact_owner_form = VerificationOwnerForm(request.POST or None, instance=instance)

    uploaded_docs = [
        {"name": 'Lease Agreement 2015', "filename": 'lease2015.pdf', "added": "Jan. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Deed with signature', "filename": 'deed_updated.pdf', "added": "Sep, 16, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Notice to evict - copy', "filename": 'eviction_notice_9_1_15.pdf', "added": "Sep. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"}
    ]

    if case_details_form.is_valid():
        case = case_details_form.save()
        messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')

        return HttpResponseRedirect('/workflow/case/%d' % case.id)

    if contact_owner_form.is_valid():
        case = contact_owner_form.save()
        messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')

        return HttpResponseRedirect('/workflow/case/%d' % case.id)

    return render(
        request,
        'workflow/verification.html',
        {
            'case_assignees': CSSCaseAssignee.objects.filter(case=instance).values_list('assignee_name', flat=True),
            'case_details_form': case_details_form,
            'contact_owner_form': contact_owner_form,
            'uploaded_docs': uploaded_docs,
            'property_address': "{} {}".format(instance.address_number, instance.street_name.capitalize()),
            'case_id': instance.pk
        }
    )
