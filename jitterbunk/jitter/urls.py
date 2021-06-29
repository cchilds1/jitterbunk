from django.conf.urls import url

from . import views

app_name='jitter'
urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.main_feed, name='main_feed'),
    url(r'^(?P<column>[-\w]+)/$', views.main_feed, name='main_feed'),
    url(r'^(?P<username>[a-zA-z\s.0-9]+)/personal_feed$', views.personal_feed, name='personal_feed'),
    url(r'^(?P<username>[a-zA-z\s.0-9]+)/(?P<column_inbox>[-\w]+)/(?P<column_sent>[-\w]+)/personal_feed$', views.personal_feed, name='personal_feed'),
    url(r'^(?P<username>[a-zA-z\s.0-9]+)/add_bunk$', views.add_bunk, name='add_bunk'),
    url(r'^(?P<username>[a-zA-z\s.0-9]+)/logout$', views.logout, name='logout'),
]
