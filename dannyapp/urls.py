from django.urls import path
from . import views
from .feeds import Latest_leet_feed, Latest_thoughts_feed, General_feed


app_name = "dannyapp"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('log/', views.log, name='log'),
    path('log/<int:year>/<int:month>/<int:day>/<slug:log>/', views.log_detail, name='log_detail'),
    path('leet', views.leet, name='leet'),
    path('leet/<slug:tag_slug>/', views.leet, name='leet_tag'),
    path('leet/<int:year>/<int:month>/<int:day>/<slug:leet>/', views.leet_detail, name='leet_detail'),
    path('<int:id>/leet_share/', views.leet_share, name='leet_share'),
    path('<int:leet_id>/comment/', views.leet_comments, name='leet_comments'),
    path('leet-feed/', Latest_leet_feed(), name='latest_leet_feed'),
    path('thoughts/', views.thoughts, name="thoughts"),
    path('thoughts/<slug:tag_slug>/', views.thoughts, name='thoughts_tag'),
    path('thoughts/<int:year>/<int:month>/<int:day>/<slug:article_slug>/', views.thoughts_detail, name="thoughts_detail"),
    path('<int:id>/thought_share/', views.thoughts_share, name="thought_share"),
    path('<int:thought_id>/thoughts-comment/', views.thoughts_comments, name="thoughts_comments"),
    path('thoughts-feed/', Latest_thoughts_feed(), name='latest_thoughts_feed'),
    path('general-feed/', General_feed(), name="general_feed"),
    path('describe/', views.description, name="description"),
    path('resume/', views.resume, name="resume"),
    path('search/', views.post_search, name="post_search"),

]