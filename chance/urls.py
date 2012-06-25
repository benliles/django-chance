from django.conf.urls.defaults import *
from django.views import generic


from chance import views, models



urlpatterns = patterns('',
    url(r'^$', generic.ListView.as_view(model=models.Event), name='chance_event_list'),
    url(r'^(?P<pk>\d+)/$', generic.DetailView.as_view(model=models.Event),
        name='chance_event'),
    url(r'^(?P<event>\d+)/register/', views.CreateRegistrationView.as_view(),
        name='chance_event_registration'),
)
