# Generated by Django 5.0.1 on 2024-02-08 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]