# Generated by Django 5.0.6 on 2024-10-26 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ulasan', '0002_alter_moodentry_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MoodEntry',
            new_name='UlasanEntry',
        ),
    ]
