# Generated by Django 5.0.1 on 2024-03-07 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifi', '0009_chatthread_is_ended_delete_notification'),
        ('service', '0002_alter_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='image',
            field=models.ImageField(blank=True, upload_to='chat_images/'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]