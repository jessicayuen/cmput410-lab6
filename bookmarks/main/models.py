from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    # Many to many foreign key
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title
