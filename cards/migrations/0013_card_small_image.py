# Generated by Django 5.1.2 on 2024-11-21 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_alter_card_archetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='small_image',
            field=models.ImageField(default='card_images/default.jpg', upload_to='small_card_images/'),
        ),
    ]