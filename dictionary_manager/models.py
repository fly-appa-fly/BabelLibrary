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


class Translation(models.Model):
    translation_to = models.ForeignKey(Language)
    translation = models.TextField()


class Word(models.Model):
    word = models.CharField(max_length=200, default='')
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    definitions = models.ManyToManyField(Definitions)
    translations = models.ManyToManyField(Translation)

    def __str__(self):
        return self.word
