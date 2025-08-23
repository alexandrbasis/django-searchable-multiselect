from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("new", "New"),
            ("old", "Old"),
            ("archived", "Archived"),
        ],
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
