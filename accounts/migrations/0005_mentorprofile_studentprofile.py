# Generated by Django 5.2.1 on 2025-05-23 10:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(max_length=100)),
                ('years_of_experience', models.PositiveIntegerField()),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('languages', models.CharField(max_length=200)),
                ('certifications', models.TextField(blank=True)),
                ('linkedin_profile', models.URLField(blank=True)),
                ('github_profile', models.URLField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_sessions', models.PositiveIntegerField(default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
                ('learning_goals', models.TextField()),
                ('interests', models.CharField(max_length=200)),
                ('preferred_languages', models.CharField(max_length=200)),
                ('github_profile', models.URLField(blank=True)),
                ('total_sessions', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
