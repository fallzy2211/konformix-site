from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import StaticViewSitemap
from core.views import healthz, robots_txt

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("healthz", healthz, name="healthz"),
    path("robots.txt", robots_txt, name="robots"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("core.urls")),
]

handler404 = "core.views.handler404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
