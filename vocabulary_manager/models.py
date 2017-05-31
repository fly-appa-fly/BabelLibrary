from django.db import models
from user_manager.models import Language
from dictionary_manager.models import Word
from django.contrib.auth.models import User


class VocabularyWord(models.Model):
    word = models.ForeignKey(Word)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    last_review = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word.word