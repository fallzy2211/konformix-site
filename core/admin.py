from django.contrib import admin

from .models import Article, Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "full_name",
        "organisation",
        "country",
        "interest",
        "source",
        "handled",
    )
    list_filter = ("handled", "source", "interest", "country", "created_at")
    search_fields = ("full_name", "email", "organisation", "job_title", "message")
    list_editable = ("handled",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    fieldsets = (
        ("Contact", {"fields": ("full_name", "email", "phone", "job_title")}),
        ("Établissement", {"fields": ("organisation", "country")}),
        ("Demande", {"fields": ("interest", "message", "source", "consent", "created_at")}),
        ("Suivi commercial", {"fields": ("handled", "internal_notes")}),
    )

    @admin.action(description="Marquer comme traité")
    def mark_handled(self, request, queryset):
        queryset.update(handled=True)

    actions = ["mark_handled"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
