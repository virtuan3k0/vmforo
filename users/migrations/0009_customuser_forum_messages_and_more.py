# Generated by Django 5.0.7 on 2024-08-10 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_subscription_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='forum_messages',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='subscription_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('trial', 'Trial')], default='inactive'),
        ),
    ]
