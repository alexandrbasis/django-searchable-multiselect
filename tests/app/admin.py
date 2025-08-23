from django.contrib import admin

from django_admin_multi_select_filter.filters import MultiSelectRelatedFieldListFilter
from tests.app.models import Item, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = (("tags", MultiSelectRelatedFieldListFilter),)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
