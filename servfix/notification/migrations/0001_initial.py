# Generated by Django 5.0.1 on 2024-04-04 15:52

import django.db.models.deletion
import notification.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('service', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ended', models.BooleanField(default=False)),
                ('participants', models.ManyToManyField(related_name='chat_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.chatthread')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_description', models.TextField()),
                ('city', models.CharField(blank=True, choices=[('Cairo', 'Cairo'), ('Alexandria', 'Alexandria'), ('Giza', 'Giza'), ('Luxor', 'Luxor'), ('Aswan', 'Aswan'), ('Damietta', 'Damietta'), ('Port Said', 'Port Said'), ('Suez', 'Suez'), ('Ismailia', 'Ismailia'), ('Faiyum', 'Faiyum'), ('Beni Suef', 'Beni Suef'), ('Minya', 'Minya'), ('Assiut', 'Assiut'), ('Sohag', 'Sohag'), ('Qena', 'Qena'), ('Red Sea', 'Red Sea'), ('New Valley', 'New Valley'), ('Matrouh', 'Matrouh'), ('Kafr El Sheikh', 'Kafr El Sheikh'), ('Monufia', 'Monufia'), ('Dakahlia', 'Dakahlia'), ('Sharqia', 'Sharqia'), ('North Sinai', 'North Sinai'), ('South Sinai', 'South Sinai'), ('Beheira', 'Beheira'), ('Gharbia', 'Gharbia'), ('Qalyubia', 'Qalyubia')], max_length=20, null=True)),
                ('additional_details', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='post_images/', validators=[notification.models.validate_image_extension])),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.post')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.providerprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]