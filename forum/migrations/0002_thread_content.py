# Generated by Django 5.0.7 on 2024-08-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='content',
            field=models.TextField(default='contenido default'),
            preserve_default=False,
        ),
    ]
