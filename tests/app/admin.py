from django.contrib import admin

from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter, MultiSelectRelatedFieldListFilter
from tests.app.models import Item, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = (
        ("tags", MultiSelectRelatedFieldListFilter),
        ("status", MultiSelectFieldListFilter),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
