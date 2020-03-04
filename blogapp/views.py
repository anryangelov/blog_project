from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from blogapp import models


class BlogsListView(ListView):

    model = models.Blog
    template_name = 'blogapp/blogs_list.html'
    paginate_by = 5


class BlogDetailView(DetailView):

    model = models.Blog
    template_name = 'blogapp/blog_detail.html'


class BloggerDetailView(DetailView):

    model = models.Blogger
    template_name = 'blogapp/blogger_detail.html'


class BloggersListView(ListView):

    model = models.Blogger
    template_name = 'blogapp/bloggers_list.html'
    paginate_by = 5


class CommentCreateView(LoginRequiredMixin, CreateView):

    model = models.Comment
    fields = ['comment']
    template_name = 'blogapp/comment_create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['blog'] = models.Blog.objects.get(pk=self.kwargs['blog_id'])
        return data

    def form_valid(self, form):
        form.instance.blog = models.Blog.objects.get(pk=self.kwargs['blog_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.blog.get_absolute_url()
