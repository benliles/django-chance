from django.conf.urls.defaults import *
from django.conf import settings
from django.views import generic


from chance import views, models



CHANCE_PREFIX = getattr(settings, 'CHANCE_URL_PREFIX', 'chance').strip('/')

urlpatterns = patterns('',
    url(r'^%s/$' % (CHANCE_PREFIX,),
        generic.ListView.as_view(model=models.Event),
        name='chance_event_list'),
    url('^(?P<slug>[\w/\-]+)$', views.EventView.as_view(slug_field='url'),
        name='chance_event'),
    url(r'^%s/(?P<pk>\d+)/$' % (CHANCE_PREFIX,),
        generic.DetailView.as_view(model=models.Event),
        name='chance_event'),
    url(r'^%s/(?P<event>\d+)/register/$' % (CHANCE_PREFIX,),
        views.CreateRegistrationView.as_view(),
        name='chance_event_registration'),
    url(r'^%s/(?P<event>\d+)/register/(?P<pk>\d+)/$' % (CHANCE_PREFIX,),
        views.RegistrationDetailView.as_view(),
        name='chance_registration'),
    url(r'^%s/(?P<event>\d+)/register/(?P<pk>\d+)/edit/$' % (CHANCE_PREFIX,),
        views.UpdateRegistrationView.as_view(),
        name='chance_registration_update'),
    url(r'^%s/(?P<event>\d+)/register/(?P<pk>\d+)/delete/$' % (CHANCE_PREFIX,),
        views.DeleteRegistrationView.as_view(),
        name='chance_registration_delete'),
    url(r'^%s/(?P<event>\d+)/registrations/$' % (CHANCE_PREFIX,),
        views.RegistrationListView.as_view(),
        name='chance_registrations'),
)
