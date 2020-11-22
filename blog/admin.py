from django.contrib import admin

from .models import Post, Category, Comment, PostSetting, CommentLike


# Register your models here.


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = (
        'title', 'slug'
    )
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 4
    inlines = [
        ChildrenItemInline,
    ]


class PostSettingInline(admin.TabularInline):
    model = PostSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'convert_create_date',
                    'convert_publish_date', 'draft', 'category', 'comment_count', 'author')
    search_fields = ('title',)
    list_filter = ('draft', 'category', 'author')
    date_hierarchy = 'publish_time'
    list_editable = ('draft',)
    inlines = [PostSettingInline,]
    actions = ['make_published', 'make_draft', 'allow_discoussion']

    def make_published(self, request, queryset):
        queryset.update(draft=False)

    make_published.short_description = "Exit selected post from draft"

    # def allow_discoussion(self, request, queryset):
    #     if queryset.get(postsetting):
    #           PostSetting.create()
    #     else:
    #           queryset.update(postsetting__allow_discusstion=True)

    # there is no object for update and should create object at first (maybe in models.py)

    # allow_discoussion.short_description = "allow user write comment on posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'is_confirmed', 'author',
                    'like_count', 'dislike_count')
    search_fields = ('content',)
    list_filter = ('is_confirmed',)
    date_hierarchy = 'create_at'


admin.site.register(Category, CategoryAdmin)
admin.site.register(CommentLike)
