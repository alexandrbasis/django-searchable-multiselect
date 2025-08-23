from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name
