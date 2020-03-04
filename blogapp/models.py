from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):

    class Meta:
        ordering = ['pk']

    post_date = models.DateTimeField(auto_now=True)
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.title}'

    def get_absolute_url(self):
        return reverse('blog', args=[self.pk])


class Blogger(models.Model):

    name = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return f'{self.pk} {self.name}'

    def get_absolute_url(self):
        return reverse('blogger', args=[self.pk])


class Comment(models.Model):

    post_date = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.comment[:15]}'
