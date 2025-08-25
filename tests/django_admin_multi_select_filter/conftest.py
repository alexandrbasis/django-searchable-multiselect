import pytest

from tests.factories import ItemFactory, TagFactory


@pytest.fixture
def sample_data():
    a = TagFactory(name="A")
    b = TagFactory(name="B")
    c = TagFactory(name="C")

    i1 = ItemFactory(name="i1", tags=[a, b])
    i2 = ItemFactory(name="i2", tags=[a])
    i3 = ItemFactory(name="i3", tags=[b, c])
    i4 = ItemFactory(name="i4")

    return {"tags": (a, b, c), "items": (i1, i2, i3, i4)}
