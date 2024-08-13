# Generated by Django 5.0.7 on 2024-08-12 00:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_privatemessage_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessage',
            name='recipient',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='recipients',
            field=models.ManyToManyField(related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]