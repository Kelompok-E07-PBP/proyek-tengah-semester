# Generated by Django 5.0.6 on 2024-10-26 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoodEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('waktu', models.DateField(auto_now_add=True)),
                ('nama_produk_ulas', models.CharField(max_length=255)),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('komentar', models.TextField()),
            ],
        ),
    ]
