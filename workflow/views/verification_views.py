import logging
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from workflow.models import Verification, CSSCase

from workflow.forms.verification_forms import VerificationDetailsForm

log = logging.getLogger('consolelogger')


@login_required(login_url='/admin/login/')
def verification(request, verification_id):
    instance = get_object_or_404(Verification, id=verification_id)

    verification_form = VerificationDetailsForm(request.POST or None, instance=instance)
    print verification_form

    uploaded_docs = [
        {"name": 'Lease Agreement 2015', "filename": 'lease2015.pdf', "added": "Jan. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Deed with signature', "filename": 'deed_updated.pdf', "added": "Sep, 16, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Notice to evict - copy', "filename": 'eviction_notice_9_1_15.pdf', "added": "Sep. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"}
    ]

    if verification_form.is_valid():
        verification = verification_form.save()
        messages.add_message(request, messages.SUCCESS, 'Verification successfully updated.')

        if request.POST.get('next-action') == 'Move to Case':
            if not CSSCase.objects.filter(verification=verification):
                case = CSSCase.objects.create(verification=verification)
            else:
                case = CSSCase.objects.create(verification=verification)[0]
                # add message warning that it exists
            return HttpResponseRedirect('/workflow/case/{}'.format(case.id))

        # TODO: handle other conditions
        else:
            return HttpResponseRedirect('/workflow/verifications')

    case_id = None
    cases = CSSCase.objects.filter(verification=instance)
    if cases:
        case_id = cases[0].id

    return render(
        request,
        'workflow/verification.html',
        {
            'verification_form': verification_form,
            'uploaded_docs': uploaded_docs,
            'property_address': instance.report.address,
            'verification_id': instance.pk,
            'report_id': instance.report.id,
            'case_id': case_id
        }
    )
