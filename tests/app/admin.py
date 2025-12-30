from django.contrib import admin

from django_admin_multi_select_filter.filters import (
    MultiSelectFieldListFilter,
    SearchableMultiSelectRelatedFieldListFilter,
)
from tests.app.models import Item, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "get_tags")
    list_filter = (
        ("tags", SearchableMultiSelectRelatedFieldListFilter),
        ("status", MultiSelectFieldListFilter),
    )
    search_fields = ("name", "tags__name")

    @admin.display(description="Tags")
    def get_tags(self, obj):
        return ", ".join(t.name for t in obj.tags.all())


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
