import pytest
from django.urls import reverse

from tests.app.models import Item

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

    def _get_filter_spec(self, response, filter_cls_name="MultiSelectRelatedFieldListFilter"):
        cl = response.context["cl"]
        for spec in cl.filter_specs:
            if spec.__class__.__name__ == filter_cls_name:
                return spec
        raise AssertionError("Filter spec not found")
