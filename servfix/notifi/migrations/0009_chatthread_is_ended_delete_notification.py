# Generated by Django 5.0.1 on 2024-02-21 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifi', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatthread',
            name='is_ended',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]