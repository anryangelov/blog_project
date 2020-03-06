from django.urls import path

from blogapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogsListView.as_view(), name='blogs'),
    path('<int:pk>', views.BlogDetailView.as_view(), name='blog'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger'),
    path('bloggers/', views.BloggersListView.as_view(), name='bloggers'),
    path('blog/<int:blog_id>/create', views.CommentCreateView.as_view(), name='comment_create'),
]
