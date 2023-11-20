from django.contrib import admin
from .models import Homepage, Log, Leet, CommentLeet, Thoughts, CommentThoughts, Site_description, Resume

admin.site.register(Homepage)
admin.site.register(Site_description)
admin.site.register(Resume)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'status']
    list_filter = ['created', 'updated','status']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'updated'
    ordering = ['status', 'created']

@admin.register(Leet)
class LeetAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'author', 'solve', 'status']
    list_filter = ['level', 'author', 'created', 'status']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'solve'
    ordering = ['solve', 'status']

@admin.register(CommentLeet)
class CommentLeetAdmin(admin.ModelAdmin):
    list_display = ['leet', 'name', 'email', 'created', 'active']
    list_filter = ['created', 'updated', 'active']
    search_fields = ['leet', 'content']

@admin.register(Thoughts)
class ThoughtsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish', 'status']

@admin.register(CommentThoughts)
class CommentThoughtsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'thought', 'created', 'activated']
    list_filter = ['activated', 'created', 'updated']
    search_fields = ['name', 'email', 'content']

