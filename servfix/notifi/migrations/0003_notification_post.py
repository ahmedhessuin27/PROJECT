# Generated by Django 5.0.1 on 2024-04-14 23:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifi', '0002_alter_notification_recipient2'),
        ('notification', '0005_alter_postforspecificprovider_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notification.post'),
        ),
    ]