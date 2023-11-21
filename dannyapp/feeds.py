from itertools import chain

import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Leet, Thoughts

class Latest_leet_feed(Feed):
    title = "邱冠諭的網頁"
    link = reverse_lazy("blog:leet")
    description = "最新Leetcode題解"

    def items(self):
        return Leet.solved.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.problem), 30)

    def item_solved_date(self, item):
        return item.solve

class Latest_thoughts_feed(Feed):
    title = "邱冠諭的網頁"
    link = reverse_lazy("blog:thoughts")
    description = "讀書隨筆最新文章"

    def items(self):
        return Thoughts.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.content), 30)

    def item_publish_date(self, item):
        return item.publish

class General_feed(Feed):
    title = "本站最新文章"
    link = reverse_lazy("blog:index")
    description = "本站最新文章"

    def items(self):
        leet_items = Leet.solved.all()[:5]
        thoughts_items = Thoughts.published.all()[:5]

        combined_items = sorted(chain(leet_items, thoughts_items),
                                key=lambda item: item.solve if hasattr(item, 'solve') else item.publish, reverse=True)
        return combined_items[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = item.problem if hasattr(item, 'problem') else item.content
        return truncatewords_html(markdown.markdown(content), 30)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_publish_date(self, item):
        return item.solve if hasattr(item, 'solve') else item.publish