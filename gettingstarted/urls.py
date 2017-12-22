from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import zendesk.views
import ig.views
import zendesk.metadataviews

urlpatterns = [
	# TESTING
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ticket/url/(?P<user_id>\d+)/$', hello.views.pull, name='url_parameter'),
    url(r'^ticket/get/$', hello.views.get, name='url_parameter_get'),
    url(r'^ticket/post/$', hello.views.post, name='url_parameter_post'),

    # ZENDESK TELEGRAM
    url(r'^zendesk/telegram/admin_ui$', zendesk.views.admin, name='cif_admin_ui'),
    url(r'^zendesk/telegram/pull', zendesk.views.pull, name='cif_pull'),
    url(r'^zendesk/telegram/channelback$', zendesk.views.channelback, name='cif_channelback'),
    url(r'^zendesk/telegram/clickthrough$', zendesk.views.clickthrough, name='cif_clickthrough'),
    url(r'^zendesk/telegram/manifest/$', zendesk.views.manifest, name='cif_manifest'),
    url(r'^zendesk/telegram/get_verify$', zendesk.views.get_verify, name='cif_get_verify'),
    url(r'^zendesk/telegram/send_metadata/', zendesk.views.send_metadata, name='cif_send_metadata'),

    # ZENDESK INSTAGRAM
    url(r'^zendesk/instagram/admin_ui/', ig.views.admin, name='cif_ig_admin_ui'),
    url(r'^zendesk/instagram/auth/', ig.views.adminauth, name='cif_ig_auth_code'),
    url(r'^zendesk/instagram/givetoken(?P<code>\w{0,50})/$', ig.views.givetoken, name='cif_ig_givetoken'),
    url(r'^zendesk/instagram/manifest/$', ig.views.manifest, name='cif_ig_manifest'),
    url(r'^zendesk/instagram/pull/', ig.views.pull, name='cif_ig_pull'),
    url(r'^zendesk/instagram/channelback/$', ig.views.channelback, name='cif_ig_channelback'),
    url(r'^zendesk/instagram/clickthrough/$', ig.views.clickthrough, name='cif_ig_clickthrough'),
    url(r'^zendesk/instagram/doAuth$', ig.views.doAuth, name='cif_ig_auth'),
]

handler500 = ig.views.handler500