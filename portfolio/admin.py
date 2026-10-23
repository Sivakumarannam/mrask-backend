from django.contrib import admin

from .models import ContactMessage, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_published', 'demo_kind')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('name', 'email', 'message', 'created_at')
