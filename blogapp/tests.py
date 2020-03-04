from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User

from blogapp.models import Blog, Blogger, Comment


class TestModels(TestCase):

    def test_blog_and_blogger(self):
        user = User.objects.create(username='foo', password='moo')
        blog = Blog.objects.create(
            author=user,
            title='some title',
            content='some content'
        )
        self.assertEqual(
            list(Blog.objects.all()), [blog]
        )

    def test_blog_content_field_is_None(self):
        user = User.objects.create(username='foo', password='moo')
        with self.assertRaises(IntegrityError):
            Blog.objects.create(
                author=user,
                title='Why Python',
                content=None
            )


class TestViews(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'angel',
            'password': '1111'
        }
        self.user = User(**self.credentials)
        self.user.set_password(self.credentials['password'])
        self.user.save()

        self.blogs = [Blog.objects.create(
                          author=self.user,
                          title=f'Why Python {i}',
                          content=f'Because is readable {i}')
                      for i in range(3)]

        self.bloggers = [Blogger.objects.create(
                            name=self.user,
                            bio=f'developer {i}')
                         for i in range(3)]

    def test_BlogsListView(self):
        url = reverse('blogs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogapp/blogs_list.html')
        self.assertEqual(
            list(response.context['object_list']),
            self.blogs,
        )

    def test_BloggerDetailView(self):
        response = self.client.get(self.bloggers[1].get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogapp/blogger_detail.html')
        self.assertEqual(
            response.context['object'],
            self.bloggers[1]
        )

    def test_BlogDetailView(self):
        response = self.client.get(self.blogs[1].get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogapp/blog_detail.html')
        self.assertEqual(
            response.context['object'],
            self.blogs[1]
        )

    def test_CommentCreateView_get(self):
        url = reverse('comment_create', args=[self.blogs[1].pk])
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogapp/comment_create.html')
        self.assertEqual(response.context['blog'], self.blogs[1])

    def test_CommentCreateView_post(self):
        url = reverse('comment_create', args=[self.blogs[1].pk])
        data = {'comment': 'stupid blog'}
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(url, data=data)
        self.assertRedirects(response, self.blogs[1].get_absolute_url())
        self.assertQuerysetEqual(
            Comment.objects.all(),
            [f'angel  {self.blogs[1].pk}  stupid blog'],
            lambda x: f'{x.user.username}  {x.blog.pk}  {x.comment}',
        )

    def test_CommentCreateView_post_with_bad_args(self):
        url = reverse('comment_create', args=[self.blogs[1].pk])
        data = {'comment': ''}
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            'comment',
            ['This field is required.']
        )
