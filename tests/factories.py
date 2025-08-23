import factory
from factory.django import DjangoModelFactory

from tests.app.models import Tag, Item


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"tag-{n}")


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: f"item-{n}")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for t in extracted:
                self.tags.add(t)
