# Generated by Django 4.2.7 on 2024-03-18 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbox', '0019_remove_posts_user_scrapbox_user_alter_wishlist_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('adrress', models.CharField(max_length=200)),
                ('phone_no', models.CharField(max_length=200)),
            ],
        ),
    ]
