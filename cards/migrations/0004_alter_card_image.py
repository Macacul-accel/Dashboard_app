# Generated by Django 5.1.2 on 2024-11-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_cardset_rarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(default=1, upload_to='card_images/'),
        ),
    ]