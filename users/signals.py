from django.db.models.signals import post_save
from django.dispatch import receiver
from forum.models import Thread, Post
from .models import CustomUser

@receiver(post_save, sender=Thread)
@receiver(post_save, sender=Post)
def update_forum_messages(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        thread_count = Thread.objects.filter(author=user).count()
        post_count = Post.objects.filter(author=user).count()
        user.forum_messages = thread_count + post_count
        user.save()
