from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


from chance import views, models



urlpatterns = patterns('',
    url(r'^$', generic.ListView.as_view(model=models.Event), name='chance_event_list'),
    url(r'^(?P<pk>\d+)/$', generic.DetailView.as_view(model=models.Event),
        name='chance_event'),
    url(r'^(?P<event>\d+)/register/$', views.CreateRegistrationView.as_view(),
        name='chance_event_registration'),
    url(r'^(?P<event>\d+)/register/(?P<pk>\d+)/$', views.RegistrationDetailView.as_view(),
        name='chance_registration'),
    url(r'^(?P<event>\d+)/register/(?P<pk>\d+)/edit/$', views.UpdateRegistrationView.as_view(),
        name='chance_registration_update'),
    url(r'^(?P<event>\d+)/register/(?P<pk>\d+)/delete/$', views.DeleteRegistrationView.as_view(),
        name='chance_registration_delete'),
    url(r'^(?P<event>\d+)/registrations/$',
        views.RegistrationListView.as_view(),
        name='chance_registrations'),
    url(r'^(?P<event>\d+)/talks/$', views.TalkListView.as_view(),
        name='talks'),
    url(r'^(?P<event>\d+)/talks/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='talk'),
    url(r'^(?P<event>\d+)/talks/add/$',
        login_required(views.TalkSubmissionCreateView.as_view()),
        name='submit_talk'),
    url(r'^(?P<event>\d+)/talks/(?P<pk>\d+)/update/$',
        login_required(views.TalkSubmissionUpdateView.as_view()),
        name='update_talk'),
    url(r'^(?P<event>\d+)/schedule/$',
        views.ScheduleView.as_view(),
        name='schedule'),
    url(r'^transaction/confirm/$',
        views.TransactionConfirmView.as_view(),
        name='transaction_confirm'),
    url(r'^transaction/(?P<pk>\d+)/$',
        views.TransactionView.as_view(),
        name='transaction'),
    url(r'transaction/(?P<pk>\d+)/cancel/$',
        views.TransactionCancel.as_view(),
        name='transaction_cancel'),
    url(r'transaction/(?P<pk>\d+)/success/$',
        views.TransactionView.as_view(template_name='chance/transaction_success.html'),
        name='transaction_success'),
    url(r'^transaction/notify/$',
        csrf_exempt(views.TransactionNotifyView.as_view()),
        name='transaction_notify')
)
