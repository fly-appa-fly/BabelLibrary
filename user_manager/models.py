from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    eng_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.eng_name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    native_lang = models.ForeignKey(Language, related_name='native_speakers')
    learning_langs = models.ManyToManyField(Language, related_name='learners')
    friends = models.ManyToManyField('self', symmetrical=False)