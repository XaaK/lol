from django.conf.urls import patterns, url

urlpatterns = patterns('lol.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^top/$', 'top', name='top'),
    url(r'^top/(?P<language_id>\d+)/$', 'top', name='toplang'),
    url(r'^view/(?P<snippet_id>\d+)/$', 'view', name='view'),
    url(r'^bylang/(?P<language_id>\d+)/$', 'bylang', name='bylang'),
    url(r'^about/$', 'about', name='about'),
)
