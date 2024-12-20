# Generated by Django 5.1.3 on 2024-12-07 13:09

from django.db import migrations
from django.core.management import call_command

def load_data(apps, schema_editor):
    call_command("loaddata", "products.json")

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_kategori'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
