# Generated by Django 5.1.2 on 2024-10-23 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ulasan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pengguna', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('komentar', models.TextField()),
                ('tanggal_ulasan', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
