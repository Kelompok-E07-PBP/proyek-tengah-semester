# Generated by Django 5.1.2 on 2024-10-22 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengiriman', '0002_alter_pengiriman_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pengiriman',
            name='city',
            field=models.CharField(choices=[('Jakarta Barat', 'Jakarta Barat'), ('Jakarta Pusat', 'Jakarta Pusat'), ('Jakarta Selatan', 'Jakarta Selatan'), ('Jakarta Timur', 'Jakarta Timur'), ('Jakarta Utara', 'Jakarta Utara')], max_length=100),
        ),
        migrations.AlterField(
            model_name='pengiriman',
            name='postal_code',
            field=models.IntegerField(),
        ),
    ]