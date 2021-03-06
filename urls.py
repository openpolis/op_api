from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from flashpolicies import policies
admin.autodiscover()


domain = '*'
headers = ['Authorization',]
policy = policies.Policy()
policy.allow_domain(domain)
policy.allow_headers(domain, headers)


# api and admin urls
urlpatterns = patterns('',
    (r'^op/1.0/', include('op_api.op.v1.urls')),
#    (r'^opp/', include('op_api.opp.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^crossdomain.xml$',
        'flashpolicies.views.serve',
        {'policy': policy}),
    
)


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

