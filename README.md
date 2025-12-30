# Django Searchable Multiselect

A Django admin filter library with multi-select functionality, searchable dropdown, and chips UI.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Django](https://img.shields.io/badge/django-4.2%20%7C%205.0%20%7C%205.1%20%7C%205.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Multi-select filtering** - Select multiple values for any filter
- **Searchable dropdown** - Quick search through 100+ options
- **Chips UI** - Visual tags showing selected filters with one-click removal
- **URL compatible** - Standard Django admin URL format (`?field__in=1,2,3`)
- **No jQuery required** - Pure vanilla JavaScript

## Installation

```bash
pip install git+https://github.com/alexandrbasis/django-searchable-multiselect.git
```

## Quick Start

### Basic Multi-Select Filter (no search)

No need to add to `INSTALLED_APPS`:

```python
from django.contrib import admin
from django_admin_multi_select_filter.filters import (
    MultiSelectFieldListFilter,
    MultiSelectRelatedFieldListFilter,
)

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_filter = (
        ("status", MultiSelectFieldListFilter),           # For CharField with choices
        ("category", MultiSelectRelatedFieldListFilter),  # For ForeignKey/ManyToMany
    )
```

### Searchable Multi-Select Filter (with search + chips)

Add to `INSTALLED_APPS` for template loading:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_admin_multi_select_filter",
]
```

```python
# admin.py
from django.contrib import admin
from django_admin_multi_select_filter.filters import SearchableMultiSelectRelatedFieldListFilter

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_filter = (
        ("tags", SearchableMultiSelectRelatedFieldListFilter),
    )
```

## Available Filters

| Filter | Use Case | Requires INSTALLED_APPS |
|--------|----------|------------------------|
| `MultiSelectFieldListFilter` | CharField with choices | No |
| `MultiSelectRelatedFieldListFilter` | ForeignKey, ManyToMany | No |
| `ExclusiveMultiSelectRelatedFieldListFilter` | ManyToMany with AND logic | No |
| `SearchableMultiSelectRelatedFieldListFilter` | Related fields with search UI | **Yes** |

## Filter Behavior

### Inclusive (OR) - Default
`MultiSelectRelatedFieldListFilter` - Items matching **ANY** selected value:
```
?tags__id__in=1,2,3  →  Items with tag 1 OR tag 2 OR tag 3
```

### Exclusive (AND)
`ExclusiveMultiSelectRelatedFieldListFilter` - Items matching **ALL** selected values:
```
?tags__id__in=1,2,3  →  Items with tag 1 AND tag 2 AND tag 3
```

## Screenshots

### Searchable Filter with Chips
The searchable filter shows selected items as chips and provides a search box that filters options in real-time:

- Click on the search box to open the dropdown
- Type to filter options
- Selected items appear as chips above the search
- Click × on a chip to remove the filter

## Development

```bash
# Clone and setup
git clone https://github.com/alexandrbasis/django-searchable-multiselect.git
cd django-searchable-multiselect
python -m venv venv
source venv/bin/activate
pip install -e ".[test]"

# Run tests
pytest

# Run demo
python demo/setup.py
python demo/manage.py runserver
# Open http://127.0.0.1:8000/admin/ (admin/admin)
```

## Credits

Based on [django-admin-multi-select-filter](https://github.com/JobDoesburg/django-admin-multi-select-filter) by Job Doesburg.

## License

MIT License - see [LICENSE](LICENSE) file.
