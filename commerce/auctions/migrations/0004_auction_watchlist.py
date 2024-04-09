# Generated by Django 4.2.7 on 2024-03-20 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_category_auction_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]