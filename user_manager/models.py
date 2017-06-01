from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Language(models.Model):
    eng_name = models.CharField(max_length=200)
    #is_active = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.eng_name


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    bio = models.TextField(blank=True)
    #native_lang = models.ForeignKey(Language, related_name='native_speakers')
    #learning_langs = models.ManyToManyField(Language, related_name='learners')
    friends = models.ManyToManyField('self', symmetrical=False)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()