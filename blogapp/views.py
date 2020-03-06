from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as LR
from django.shortcuts import get_object_or_404, render

from blogapp import models


def index(request):
    return render(request, 'index.html')


class BlogsListView(LR, ListView):

    model = models.Blog
    template_name = 'blogapp/blogs_list.html'
    paginate_by = 5


class BlogDetailView(LR, DetailView):

    model = models.Blog
    template_name = 'blogapp/blog_detail.html'


class BloggerDetailView(LR, DetailView):

    model = models.Blogger
    template_name = 'blogapp/blogger_detail.html'


class BloggersListView(LR, ListView):

    model = models.Blogger
    template_name = 'blogapp/bloggers_list.html'
    paginate_by = 5


class CommentCreateView(LR, CreateView):

    model = models.Comment
    fields = ['comment']
    template_name = 'blogapp/comment_create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['blog'] = get_object_or_404(
            models.Blog, pk=self.kwargs['blog_id'])
        return data

    def form_valid(self, form):
        form.instance.blog = get_object_or_404(
            models.Blog, pk=self.kwargs['blog_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.blog.get_absolute_url()
