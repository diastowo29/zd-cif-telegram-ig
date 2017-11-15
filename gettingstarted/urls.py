from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import zendesk.views

urlpatterns = [
	# TESTING
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ticket/url/(?P<user_id>\d+)/$', hello.views.pull, name='url_parameter'),
    url(r'^ticket/get/$', hello.views.get, name='url_parameter_get'),
    url(r'^ticket/post/$', hello.views.post, name='url_parameter_post'),

    # ZENDESK
    url(r'^zendesk/telegram/admin_ui/$', zendesk.views.admin, name='cif_admin_ui'),
    url(r'^zendesk/telegram/pull/$', zendesk.views.pull, name='cif_pull'),
    url(r'^zendesk/telegram/channelback/$', zendesk.views.channelback, name='cif_channelback'),
    url(r'^zendesk/telegram/clickthrough/$', zendesk.views.clickthrough, name='cif_clickthrough'),
    url(r'^zendesk/telegram/manifest/$', zendesk.views.manifest, name='cif_manifest'),
    url(r'^zendesk/telegram/admin_ui/send_metadata$', zendesk.views.send_metadata, name='cif_send_metadata'),
]
