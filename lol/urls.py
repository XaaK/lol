from django.conf.urls import patterns, url

urlpatterns = patterns('lol.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^rate/(?P<snippet_id>\d+)/$', 'rate', name='rate'),
    url(r'^top/(?P<limit>\d+)/$', 'top', name='top'),
    url(r'^view/(?P<snippet_id>\d+)/$', 'view', name='view'),
    url(r'^import_gist/$', 'import_gist', name='import_gist'),
)
