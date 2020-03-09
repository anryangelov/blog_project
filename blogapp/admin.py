from django.contrib import admin

from blogapp import models


admin.site.register(models.Blogger)
admin.site.register(models.Comment)


class BlogCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = models.Comment
    max_num = 0


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Administration object for Blog models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of blog comments in blog view (inlines)
    """
    list_display = ('title', 'author', 'post_date')
    inlines = [BlogCommentsInline]
