from django.conf.urls import patterns, url

from hadiths import views
from hadiths import apiviews

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^persons$', views.persons, name='persons'),
    url(r'^hadith/(?P<hadith_id>\d+)$', views.hadith, name='hadith'),
    url(r'^hadiths$', views.hadiths, name='hadiths'),
    # APIs
    url(r'^apis/persons/$', apiviews.PersonSetView.as_view()),
    url(r'^apis/persons/(?P<pk>[0-9]+)$', apiviews.PersonView.as_view()),
    url(r'^apis/hadithtags/$', apiviews.HadithTagSetView.as_view()),
    url(r'^apis/hadithtags/(?P<pk>[0-9]+)$', apiviews.HadithTagView.as_view()),
    url(r'^apis/hadiths/$', apiviews.HadithSetView.as_view()),
    url(r'^apis/hadiths/(?P<pk>[0-9]+)$', apiviews.HadithView.as_view())
)