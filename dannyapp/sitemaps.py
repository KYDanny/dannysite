from django.contrib.sitemaps import Sitemap
from .models import Leet, Thoughts

class LeetSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Leet.solved.all()

    def lastmod(self, obj):
        return obj.updated

class ThoughtsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Thoughts.published.all()

    def lastmod(self, obj):
        return obj.updated