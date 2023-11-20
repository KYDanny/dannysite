from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Log, Leet, Thoughts

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

#leet section
@register.simple_tag
def total_leets():
    return Leet.solved.count()

@register.inclusion_tag('dannyapp/post/includes/latest_leets.html')
def latest_leets(count=5):
    latests = Leet.solved.order_by("-solve")[:count]
    return {"latests":latests}

@register.inclusion_tag("dannyapp/post/includes/most_commented_leets.html")
def most_commented_leets(count=5):
    most_commented = Leet.solved.annotate(comment_num=Count("Comments")).order_by("-comment_num")[:count]
    return {"most_commented":most_commented}
#log section
@register.simple_tag
def total_logs():
    return Log.completed.count()

@register.inclusion_tag('dannyapp/post/includes/latest_logs.html')
def latest_logs(count=5):
    latests = Log.completed.order_by('-complete')[:count]
    return {'latests':latests}

#thoughts section
@register.simple_tag
def total_thoughts():
    return Thoughts.published.count()

@register.inclusion_tag("dannyapp/post/includes/latest_thoughts.html")
def latest_thoughts(count=5):
    latest = Thoughts.published.order_by('-publish')[:count]
    return {"latest":latest}

@register.simple_tag
def most_commented_thoughts(count=5):
    return Thoughts.published.annotate(comment_num=Count('comment_thoughts')).order_by('-comment_num')[:count]



