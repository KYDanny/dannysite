from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


#Homepage
class Homepage(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()

    def __str__(self):
        return self.title

#custom managers

class CompletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Log.Status.COMPLETE)

class SolvedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Leet.Status.SOLVED)

class ThoughtsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Thoughts.Status.PUBLISHED)

#Log model
class Log(models.Model):

    class Status(models.TextChoices):
        COMPLETE = 'C', _('complete')
        INCOMPLETE = 'I', _('incomplete')

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='complete')
    body = models.TextField()
    complete = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,
                              choices=Status.choices,
                              default=Status.INCOMPLETE)
    objects = models.Manager()
    completed = CompletedManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def get_absolute_url(self):
        return reverse('blog:log_detail', args=[self.created.year,
                                                  self.created.month,
                                                  self.created.day,
                                                  self.slug])

    def __str__(self):
        return self.title

#Leet model
class Leet(models.Model):

    class Status(models.TextChoices):
        UNSOLVED = 'UN', 'unsolved'
        SOLVED = 'SV', 'solved'

    class Level(models.TextChoices):
        EASY = 'E', 'easy'
        MEDIUM = 'M', 'medium'
        HARD = 'H', 'hard'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='solve')
    problem = models.TextField()
    solution = models.TextField(null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='leet_posts')
    solve = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.UNSOLVED)
    level = models.CharField(max_length=1,
                            choices=Level.choices,
                            default=Level.MEDIUM)
    objects = models.Manager()
    solved = SolvedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-solve']
        indexes = [
            models.Index(fields=['-solve'])
        ]

    def get_absolute_url(self):
        return reverse("blog:leet_detail", args=[self.solve.year,
                                                   self.solve.month,
                                                   self.solve.day,
                                                   self.slug])

    def __str__(self):
        return self.title

class CommentLeet(models.Model):
    leet = models.ForeignKey(Leet,
                             on_delete=models.CASCADE,
                             related_name='Comments')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"{self.name}對{self.leet}作了留言"

#thoughts
class Thoughts(models.Model):

    class Status(models.TextChoices):
        UNPUBLISHED = "UN", _('unpublished')
        PUBLISHED = "PB", _('published')

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thought_posts")
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNPUBLISHED)
    published = ThoughtsManager()
    objects = models.Manager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def get_absolute_url(self):
        return reverse("blog:thoughts_detail", args=[self.publish.year,
                                                       self.publish.month,
                                                       self.publish.day,
                                                       self.slug]) #args=[self.id]的情況，常寫成self.publish.id,  易錯。

    def __str__(self):
        return self.title

class CommentThoughts(models.Model):
    thought = models.ForeignKey(Thoughts,
                                 on_delete=models.CASCADE,
                                 related_name='comment_thoughts')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return f"Comment by {self.name} on {self.thought}"

class Site_description(models.Model):
    describe = models.TextField()

    def __str__(self):
        return "This is the description of this site."

class Resume(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    activated = models.BooleanField(default=True)

    def __str__(self):
        return self.title
