# Generated by Django 5.2.1 on 2025-07-14 10:45

import django.db.models.deletion
import user_managment.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, validators=[user_managment.models.validate_username_with_special_characters])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=225)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_advertiser', models.BooleanField(default=False)),
                ('is_channel_admin', models.BooleanField(default=False)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('female', 'FEMALE'), ('male', 'MALE')], max_length=6, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatars/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
