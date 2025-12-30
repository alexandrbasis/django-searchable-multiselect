import pytest
from django.urls import reverse

from tests.app.models import Item
from tests.factories import ItemFactory

pytestmark = pytest.mark.django_db


class TestMultiSelectRelatedFieldListFilter:
    def test_in_param_comma_separated_parses_lookup_val(self, admin_client, sample_data):
        url = reverse("admin:testapp_item_changelist")
        a, b, _ = sample_data["tags"]
        resp = admin_client.get(url, {"tags__id__in": f"{a.pk},{b.pk}"})
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)

        assert spec.lookup_kwarg == "tags__id__in"
        assert spec.lookup_kwarg_isnull == "tags__isnull"
        assert spec.lookup_val == [str(a.pk), str(b.pk)]

        qs = list(resp.context["cl"].queryset)
        i1, i2, i3, i4 = sample_data["items"]
        assert set(qs) == {i1, i2, i3}

    def test_isnull_true_filters_items_without_relations(self, admin_client, sample_data):
        url = reverse("admin:testapp_item_changelist")
        resp = admin_client.get(url, {"tags__isnull": "1"})
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_kwarg_isnull == "tags__isnull"

        qs = list(resp.context["cl"].queryset)
        i1, i2, i3, i4 = sample_data["items"]
        assert qs == [i4]

    def test_empty_value_leaves_queryset_unfiltered(self, admin_client, sample_data):
        url = reverse("admin:testapp_item_changelist")
        resp = admin_client.get(url)
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_val == []

        qs = list(resp.context["cl"].queryset)
        assert set(qs) == set(Item.objects.all())

    def _get_filter_spec(self, response, filter_cls_name="SearchableMultiSelectRelatedFieldListFilter"):
        cl = response.context["cl"]
        for spec in cl.filter_specs:
            if spec.__class__.__name__ == filter_cls_name:
                return spec


class TestMultiSelectFieldListFilter:
    def test_in_param_comma_separated_parses_lookup_val(self, admin_client):
        item_new = ItemFactory(name="A", status="new")
        item_old = ItemFactory(name="B", status="old")
        ItemFactory(name="C", status="archived")
        ItemFactory(name="D", status="")

        url = reverse("admin:testapp_item_changelist")

        resp = admin_client.get(url, {"status__in": "new,old"})
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_kwarg == "status__in"
        assert spec.lookup_kwarg_isnull == "status__isnull"
        assert spec.lookup_val == ["new", "old"]

        qs = resp.context["cl"].queryset
        assert not qs.exclude(status__in=["new", "old"]).exists()
        assert {item_new, item_old}.issubset(set(qs))

    def test_isnull_true_filters_items_with_nulls(self, admin_client):
        ItemFactory(name="E", status="")
        ItemFactory(name="F", status="new")
        url = reverse("admin:testapp_item_changelist")
        resp = admin_client.get(url, {"status__isnull": "1"})
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_kwarg_isnull == "status__isnull"

        qs = resp.context["cl"].queryset

        assert not qs.filter(status__isnull=False).exists()

    def test_empty_value_leaves_queryset_unfiltered(self, admin_client):
        ItemFactory(name="G", status="new")
        ItemFactory(name="H", status="")
        url = reverse("admin:testapp_item_changelist")

        resp = admin_client.get(url)
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_val == []

        qs = list(resp.context["cl"].queryset)
        assert set(qs) == set(Item.objects.all())

    def test_empty_string_param_turns_into_empty_selection(self, admin_client):
        url = reverse("admin:testapp_item_changelist")

        resp = admin_client.get(url, {"status__in": ""})
        assert resp.status_code == 200

        spec = self._get_filter_spec(resp)
        assert spec.lookup_val == []

    def _get_filter_spec(self, response):
        cl = response.context["cl"]
        for spec in cl.filter_specs:
            if spec.__class__.__name__ == "MultiSelectFieldListFilter":
                return spec
