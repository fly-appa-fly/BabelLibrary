import datetime
import math
from django.db import models

from user_manager.models import Language
from dictionary_manager.models import Word
from django.contrib.auth.models import User


class VocabularyWord(models.Model):
    word = models.ForeignKey(Word)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    easiness_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    last_review = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word.word

    def calculate_ef(self, quality):
        self.easiness_factor += (0.1-(5-quality)*(0.08+(5-quality)*0.02))
        self.save()

    def calculate_interval(self):
        if self.repetitions == 0:
            self.interval = 0
        elif self.repetitions == 1:
            self.interval = 1
        elif self.repetitions == 2:
            self.interval = 6
        else:
            self.interval *= self.easiness_factor
        self.repetitions += 1
        self.save()

    def next_time(self):
        return self.last_review + datetime.timedelta(days=math.ceil(self.interval))

