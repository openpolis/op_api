from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# api and admin urls
urlpatterns = patterns('',
    (r'^op/v1/', include('op_api.op.v1_free.urls')),
    (r'^op/1.0/', include('op_api.op.v1_oauth.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^crossdomain.xml$',
        'flashpolicies.views.simple',
        {'domains': ['*']}),
    
)

# OAUTH three-legged
# urlpatterns += patterns(
#    'piston.authentication',
#    url(r'^oauth/request_token/$','oauth_request_token', name='oauth_request_token'),
#    url(r'^oauth/authorize/$','oauth_user_auth', name='oauth_user_auth'),
#    url(r'^oauth/access_token/$','oauth_access_token', name='oauth_access_token'),
#)


# static media (not for production!)
if (settings.ENVIRONMENT != 'production'):
  urlpatterns += patterns('',
    (r'^robots.txt$', 'django.views.static.serve', 
      { 'path' : "/robots.txt", 
        'document_root': settings.TEMPLATE_DIRS[0],
        'show_indexes': False } ),
    (r'^favicon.ico$', 'django.views.static.serve', 
      { 'path' : "/favicon.ico", 
        'document_root': settings.TEMPLATE_DIRS[0],
        'show_indexes': False } ),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/css" % settings.TEMPLATE_DIRS[0]}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/images" % settings.TEMPLATE_DIRS[0]}),
  )

