from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


from chance import views, models



urlpatterns = patterns('',
    url(r'^(?P<slug>\w+)/register/$', views.CreateRegistrationView.as_view(),
        name='register'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/$', views.RegistrationDetailView.as_view(),
        name='registration'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/edit/$', views.UpdateRegistrationView.as_view(),
        name='registration_update'),
    url(r'^(?P<slug>\w+)/register/(?P<pk>\d+)/delete/$', views.DeleteRegistrationView.as_view(),
        name='registration_delete'),
    url(r'^(?P<slug>\w+)/register/registrations/$',
        views.RegistrationListView.as_view(),
        name='registrations'),
    url(r'^(?P<slug>\w+)/talks/$', views.TalkListView.as_view(),
        name='talks'),
    url(r'^(?P<slug>\w+)/talks/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='talk'),
    url(r'^(?P<slug>\w+)/talks/add/$',
        login_required(views.TalkSubmissionCreateView.as_view()),
        name='submit_talk'),
    url(r'^(?P<slug>\w+)/talks/(?P<pk>\d+)/update/$',
        login_required(views.TalkSubmissionUpdateView.as_view()),
        name='update_talk'),
    url(r'^(?P<slug>\w+)/schedule/$',
        views.ScheduleView.as_view(),
        name='schedule'),
)
