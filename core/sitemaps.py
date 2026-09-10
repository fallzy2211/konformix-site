from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import PRODUCTS
from .models import Article


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        pages = ["home", "products", "about", "resources", "contact"]
        pages += [("product_detail", p["key"]) for p in PRODUCTS]
        pages += [("article_detail", a.slug) for a in Article.objects.filter(is_published=True)]
        return pages

    def location(self, item):
        if isinstance(item, tuple):
            name, arg = item
            return reverse(name, args=[arg])
        return reverse(item)
