from django.db import models
from user_manager.models import Language


class Definition(models.Model):
    definition = models.TextField()

    def __str__(self):
        return self.definition


class Definitions(models.Model):
    type = models.TextField()
    definitions = models.ManyToManyField(Definition)
    additional_information = models.TextField(null=True)

    def __str__(self):
        return self.type


class Word(models.Model):
    word = models.CharField(max_length=200, default='')
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    definitions = models.ManyToManyField(Definitions)

    def __str__(self):
        return self.word
