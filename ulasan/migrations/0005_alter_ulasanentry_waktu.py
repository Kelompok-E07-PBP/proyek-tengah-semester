# Generated by Django 5.0.6 on 2024-10-26 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulasan', '0004_remove_ulasanentry_nama_ulasanentry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ulasanentry',
            name='waktu',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]