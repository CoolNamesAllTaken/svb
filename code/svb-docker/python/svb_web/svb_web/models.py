from django.db import models
from django.utils import timezone


class Metadata(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    # Metadata
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        now = timezone.now()
        if self._state.adding:
            self.date_created = now
        self.date_modified = now
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        abstract = True


class NewsAuthor(Metadata):
    name = models.CharField(max_length=32)  # "Jane Doe"
    title = models.CharField(max_length=64, blank=True, null=True)  # "Candy QA"


class NewsArticle(Metadata):
    headline = models.CharField(max_length=128)  # "Shrinkflation: King Size Candy 20% Smaller"
    author = models.ForeignKey('NewsAuthor', on_delete=models.RESTRICT)
    date_published = models.DateTimeField()
