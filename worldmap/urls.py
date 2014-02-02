from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from worldmap.sitemap import LayerSitemap, MapSitemap
import worldmap.proxy.urls
import worldmap.maps.urls
import worldmap.gazetteer.urls
import worldmap.mapnotes.urls
import worldmap.capabilities.urls


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import autocomplete_light
autocomplete_light.autodiscover()
admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('geonode',)
}

sitemaps = {
    "layer": LayerSitemap,
    "map": MapSitemap
}

urlpatterns = patterns('',

    # Static pages
    url(r'^$', 'django.views.generic.simple.direct_to_template',
                {'template': 'index.html'}, name='home'),
    url(r'^developer/$', 'django.views.generic.simple.direct_to_template',
                {'template': 'developer.html'}, name='dev'),
    url(r'^upload_terms/$', 'django.views.generic.simple.direct_to_template',
            {'template': 'maps/upload_terms.html'}, name='upload_terms'),
     # Data views
    (r'^data/', include(worldmap.maps.urls.datapatterns)),
    (r'^maps/', include(worldmap.maps.urls.urlpatterns)),
    (r'^annotations/', include(worldmap.mapnotes.urls.urlpatterns)),
    (r'^comments/', include('dialogos.urls')),
    (r'^ratings/', include('agon_ratings.urls')),
    (r'^capabilities/', include('worldmap.capabilities.urls')),
    # Accounts
    url(r'^accounts/ajax_login$', 'worldmap.views.ajax_login',
        name='auth_ajax_login'),
    url(r'^accounts/ajax_lookup$', 'worldmap.views.ajax_lookup',
        name='auth_ajax_lookup'),
    (r'^accounts/ajax_lookup_email$', 'worldmap.views.ajax_lookup_email'),

    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^accounts/logout', 'django.contrib.auth.views.logout'),

    # Meta
    url(r'^lang\.js$', 'django.views.generic.simple.direct_to_template',
         {'template': 'lang.js', 'mimetype': 'text/javascript'}, name='lang'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog',
        js_info_dict, name='jscat'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                                  {'sitemaps': sitemaps}, name='sitemap'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/', include(admin.site.urls)),
    (r'^affiliation/confirm', 'worldmap.register.views.confirm'),
    (r'^avatar/', include('avatar.urls')),
    (r'^accounts/', include('worldmap.register.urls')),
    (r'^profiles/', include('worldmap.profile.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^download/(?P<service>[^/]*)/(?P<layer>[^/]*)/(?P<format>[^/]*)/?$','worldmap.proxy.views.download'),
    (r'^gazetteer/', include('worldmap.gazetteer.urls')),
    (r'^bostonhoods/?', include('worldmap.hoods.urls')),
    (r'^certification/', include('worldmap.certification.urls')),    
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    )

urlpatterns += worldmap.proxy.urls.urlpatterns


official_site_url_patterns = patterns('',
    (r'^tweetmap/$', 'worldmap.maps.views.tweetview'),
    (r'^(?P<site>[A-Za-z0-9_\-]+)/$', 'worldmap.maps.views.official_site'),
    (r'^(?P<site>[A-Za-z0-9_\-]+)/mobile/?$', 'worldmap.maps.views.official_site_mobile'),
    (r'^(?P<site>[A-Za-z0-9_\-]+)/info$', 'worldmap.maps.views.official_site_controller'),
)

urlpatterns += official_site_url_patterns

# Extra static file endpoint for development use
if settings.SERVE_MEDIA:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))

# Serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
