from itertools import chain

from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, ExpressionWrapper, F, FloatField
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from taggit.models import Tag
from .models import Index, Log, Leet, Thoughts, Site_description, Resume
from .forms import EmailLeetForm, CommentLeetForm, EmailThoughtsForm, CommentThoughtsForm, SearchForm

def index(request):
    posts = Index.objects.all()
    return render(request, 'dannyapp/post/index.html', {'posts':posts})

#log views
def log(request):
    logging_list = Log.completed.all()
    paginator = Paginator(logging_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        loggings = paginator.page(page_number)
    except EmptyPage:
        loggings = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        loggings = paginator.page(1)
    return render(request, 'dannyapp/post/log.html',
                  {"loggings": loggings})

def log_detail(request, year, month, day, log):
    try:
        logging = Log.completed.get(created__year=year,
                                    created__month=month,
                                    created__day=day,
                                    slug=log)
    except Log.DoesNotExist:
        raise Http404("No Post Found")

    return render(request, 'dannyapp/post/log_detail.html', {'logging':logging})

#leet views
def leet(request, tag_slug=None):
    leet_list = Leet.solved.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        leet_list = leet_list.filter(tags__in=[tag])
    paginator = Paginator(leet_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        leets = paginator.page(page_number)
    except EmptyPage:
        leets = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        leets = paginator.page(1)
    return render(request, 'dannyapp/post/leet.html', {"leets":leets, "tag":tag})

def leet_detail(request, year, month, day, leet):
    leet = get_object_or_404(Leet,
                             status=Leet.Status.SOLVED,
                             solve__year=year,
                             solve__month=month,
                             solve__day=day,
                             slug=leet)
    tags_ids = leet.tags.values_list('id', flat=True)
    similar_leets = Leet.objects.filter(tags__in=tags_ids).exclude(id=leet.id)
    similar_leets = similar_leets.annotate(same_leets=Count('tags')).order_by('-same_leets', '-solve')[:4]
    comments = leet.Comments.filter(active=True)
    form = CommentLeetForm()
    return render(request, "dannyapp/post/leet_detail.html", {"leet":leet, "comments":comments,\
                                                            "form":form, "similar_leets":similar_leets})

def leet_share(request, id):
    leet = get_object_or_404(Leet,
                             id=id,
                             status=Leet.Status.SOLVED)
    sent = False
    if request.method == 'POST':
        form = EmailLeetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            share_url = request.build_absolute_uri(leet.get_absolute_url())
            subject = f"{cd['name']}推薦您閱讀{leet.title}"
            message = f"{leet.title}的連結：{share_url}\n\n{cd['name']}的留言：{cd['comment']}"
            try:
                send_mail(subject, message, cd['sender'], [cd['receiver']])
                sent = True
            except:
                return HttpResponse("發送郵件失敗")
    else:
        form = EmailLeetForm()

    return render(request, "dannyapp/post/leet_share.html", {"leet":leet, "form":form,"sent":sent})

@require_POST
def leet_comments(request, leet_id):
    leet = get_object_or_404(Leet, id=leet_id, status=Leet.Status.SOLVED)
    form = CommentLeetForm(request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.leet = leet
        comment.save()

    return render(request, "dannyapp/post/leet_comment.html", {"leet":leet, "form":form, "comment":comment})

def thoughts(request, tag_slug=None):
    thought_list = Thoughts.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        thought_list = thought_list.filter(tags__in=[tag])
    paginator = Paginator(thought_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        thoughts = paginator.page(page_number)
    except EmptyPage:
        thoughts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        thoughts = paginator.page(1)
    return render(request, "dannyapp/post/thoughts.html", {"thoughts":thoughts,
                                                         "tag":tag})

def thoughts_detail(request, year, month, day, article_slug):
    article = get_object_or_404(Thoughts, status=Thoughts.Status.PUBLISHED,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day,
                                slug=article_slug)
    tag_ids = article.tags.values_list('id', flat=True)
    related_articles = Thoughts.objects.filter(tags__id__in=tag_ids).exclude(id=article.id)
    related_articles = related_articles.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    comments = article.comment_thoughts.filter(activated=True)
    form = CommentThoughtsForm()
    return render(request, "dannyapp/post/thoughts_detail.html", {"article":article,
                                                                "form":form, "comments":comments, "related_articles":related_articles})

def thoughts_share(request, id):
    thought = get_object_or_404(Thoughts,
                                id=id,
                                status=Thoughts.Status.PUBLISHED)
    sent = False
    name = ''
    purpose = ''
    comment = ''
    receiver = ''

    if request.method == 'POST':
        form = EmailThoughtsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            link = request.build_absolute_uri(thought.get_absolute_url)
            subject = f"{cd['name']} recommends you to read {thought.title}."
            message = (f"{cd['purpose']}<br><br>"
                       f"<strong>{cd['name']}'s comment:</strong> {cd['comment']}<br><br>"
                       f"Read <strong>{thought.title}</strong> at {link}.")
            try:
                send_mail(subject, message, cd['email'], [cd['receiver']], html_message=message)
                sent = True
                name = cd['name']
                purpose = cd['purpose']
                comment = cd['comment']
                receiver = cd['receiver']
            except Exception as e:
                print("error:",e)
                return HttpResponse("發送郵件失敗")

    else:
        form = EmailThoughtsForm()

    return render(request, "dannyapp/post/thoughts_share.html", {"thought":thought,
                                                               "form":form, "sent":sent,
                                                               "name":name, "purpose":purpose,
                                                               "comment":comment, "receiver":receiver})

@require_POST
def thoughts_comments(request, thought_id):
    thought = get_object_or_404(Thoughts, id=thought_id, status=Thoughts.Status.PUBLISHED)
    form = CommentThoughtsForm(request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.thought = thought
        comment.save()
    return render(request, "dannyapp/post/thoughts_comment.html", {"thought":thought,
                                                                 "form":form, "comment":comment})

#description
def description(request):
    describes = Site_description.objects.all()

    return render(request, "dannyapp/post/describe.html", {"describes":describes})

def resume(request):
    autobio = Resume.objects.all()

    return render(request, "dannyapp/post/resume.html", {"autobio":autobio})


def post_search(request):
    form = SearchForm()
    query = ''
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            leet_results = Leet.solved.annotate(title_similarity=TrigramSimilarity('title', query),
                                                problem_similarity=TrigramSimilarity('problem', query),
                                                solution_similarity=TrigramSimilarity('solution', query)
                                                ).annotate(combined_similarity=ExpressionWrapper(
                (F('title_similarity')+F('problem_similarity')+F('solution_similarity')) / 2, output_field=FloatField())).\
                filter(combined_similarity__gt=0.1).order_by('-combined_similarity')

            thoughts_results = Thoughts.published.annotate(title_similarity=TrigramSimilarity('title', query),
                                                           content_similarity=TrigramSimilarity('content', query)
                                                           ).annotate(combined_similarity=ExpressionWrapper(
                (F('title_similarity')+F('content_similarity')) / 2, output_field=FloatField())).filter(combined_similarity__gt=0.1).\
                order_by('-combined_similarity')

            combined_results = list(chain(leet_results, thoughts_results))
            results = sorted(combined_results, key=lambda item: item.combined_similarity, reverse=True)

    return render(request, 'dannyapp/post/search.html', {"form":form, "query":query, "results":results})
