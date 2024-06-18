from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    facebook_id = models.CharField(max_length=128, null=True)
    profile_image = models.CharField(max_length=512, null=True)


class ChatMessage(TimeStampedModel):
    """
        received: Message from the User
        bot_message: Reply Message from the Bot i.e. ChatGPT
        user: The User object who sent the message
    """

    message = models.TextField()
    bot_message = models.TextField()
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'updated'])
        ]



