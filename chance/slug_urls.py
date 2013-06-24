from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


from chance import views, models



urlpatterns = patterns('',
    url(r'^(?P<slug>\w+)/register/$', views.CreateRegistrationView.as_view(),
        name='chance_event_registration_slug'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/$', views.RegistrationDetailView.as_view(),
        name='chance_registration_slug'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/edit/$', views.UpdateRegistrationView.as_view(),
        name='chance_registration_update_slug'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/delete/$', views.DeleteRegistrationView.as_view(),
        name='chance_registration_delete_slug'),
    url(r'^(?P<slug>\d+)/registrations/$',
        views.RegistrationListView.as_view(),
        name='chance_registrations_slug'),
    url(r'^(?P<slug>\w+)/talks/$', views.TalkListView.as_view(),
        name='talks_slug'),
    url(r'^(?P<slug>\w+)/talks/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='talk_slug'),
    url(r'^(?P<slug>\w+)/talks/add/$',
        login_required(views.TalkSubmissionCreateView.as_view()),
        name='submit_talk_slug'),
    url(r'^(?P<slug>\w+)/talks/(?P<pk>\d+)/update/$',
        login_required(views.TalkSubmissionUpdateView.as_view()),
        name='update_talk_slug'),
    url(r'^(?P<slug>\w+)/schedule/$',
        views.ScheduleView.as_view(),
        name='schedule_slug'),
)
