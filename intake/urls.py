from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # new call-in related urls
    url(r'^intake/step-one/$', 'intake.views.step_one', name='step_one'),
    url(r'^intake/step-two/$', 'intake.views.step_two', name='step_two'),
    url(r'^intake/step-three/$', 'intake.views.step_three', name='step_three'),
    url(r'^intake/step-four/$', 'intake.views.step_four', name='step_four'),
    url(r'^intake/step-five/$', 'intake.views.step_five', name='step_five'),
    url(r'^intake/step-six/$', 'intake.views.step_six', name='step_six'),
    url(r'^intake/step-seven/$', 'intake.views.step_seven', name='step_seven'),
    url(r'^intake/step-eight/$', 'intake.views.step_eight', name='step_eight'),
    url(r'^intake/step-nine/$', 'intake.views.step_nine', name='step_nine'),
    url(r'^intake/step-ten/$', 'intake.views.step_ten', name='step_ten'),
    url(r'^intake/step-eleven/$', 'intake.views.step_eleven', name='step_eleven'),
    url(r'^intake/step-twelve/$', 'intake.views.step_twelve', name='step_twelve'),
    url(r'^intake/step-thirteen/$', 'intake.views.step_thirteen', name='step_thirteen'),
    url(r'^intake/step-fourteen/$', 'intake.views.step_fourteen', name='step_fourteen'),

    # web intake-related urls
    url(r'^report/$', 'intake.views.report_intro', name='report_intro'),
    url(r'^report/$', 'intake.views.report_intro', name='report_intro'),
    url(r'^report/issue/$', 'intake.views.report_issue', name='report_issue'),
    url(r'^report/contact/$', 'intake.views.report_contact', name='report_contact'),
    url(r'^report/finish/$', 'intake.views.report_finish', name='report_finish'),

    # old call-in related urls (TODO: deprecate)
    url(r'^intake/welcome/$', 'intake.views.welcome', name='welcome'),
    url(r'^intake/handle-name/$', 'intake.views.handle_name', name='handle_name'),
    url(r'^intake/handle-name-transcription/$', 'intake.views.handle_name_transcription', name='handle_name_transcription'),
    url(r'^intake/handle-feedback-pref/$', 'intake.views.handle_feedback_pref', name='handle_feedback_pref'),
    url(r'^intake/handle-feedback-number/$', 'intake.views.handle_feedback_number', name='handle_feedback_number'),
    url(r'^intake/handle-problem-address/$', 'intake.views.handle_problem_address', name='handle_problem_address'),
    url(r'^intake/handle-problem-address-transcription/$', 'intake.views.handle_problem_address_transcription', name='handle_problem_address_transcription'),
    url(r'^intake/handle-problem-description/$', 'intake.views.handle_problem_description', name='handle_problem_description'),
    url(r'^intake/handle-problem-description-transcription/$', 'intake.views.handle_problem_description_transcription', name='handle_problem_description_transcription'),
)
