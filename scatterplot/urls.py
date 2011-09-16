from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('scatterplot.views',
    url(r'auth/$', 'auth', name='scatterplot_auth'),
    url(r'data/$', 'data', name='scatterplot_data'),
    url(r'$', 'home', name='scatterplot_home'),
)