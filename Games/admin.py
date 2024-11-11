from django.contrib import admin
from .models import Publisher, Game

# Register your models here.

admin.site.register(Publisher)
admin.site.register(Game)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'website')
    search_fields = ('name', 'location')

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'release_date', 'genre')
    search_fields = ('title', 'publisher__name')
    list_filter = ('genre', 'onWindows', 'onLinux', 'onMac')
    date_hierarchy = 'release_date'
    ordering = ('-release_date', 'title')
    filter_horizontal = ('publisher',)
    