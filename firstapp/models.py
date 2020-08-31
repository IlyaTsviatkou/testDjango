from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.indexes import GinIndex

class City(models.Model):
    name = models.CharField(max_length=20)

class Number(models.Model):
    name = models.CharField(max_length=20)

class Organisation(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    city = models.ManyToManyField(City)
    number = models.ManyToManyField(Number)
    class Meta:
        indexes =[GinIndex(fields=['name'])]

class Course(models.Model):
    name = models.CharField(max_length=20)
    stage = models.IntegerField() 
    class Meta:
        indexes =[GinIndex(fields=['name'])]

class Player(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    org = models.OneToOneField(Organisation, on_delete=models.CASCADE,primary_key=True)
    course = models.ManyToManyField(Course,related_name='course',symmetrical=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    stbool = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Feedback(models.Model):
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)
    email_reply_date = models.DateTimeField("Время отправки", null=True, blank=True)
    email_reply_adress = models.ManyToManyField(Profile, limit_choices_to={"verified": False}, blank=True)