from django.conf.urls.defaults import *
from django.views import generic


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
)
