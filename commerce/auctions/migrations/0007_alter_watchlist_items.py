# Generated by Django 4.2.7 on 2024-03-20 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_watchlist_items_alter_watchlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='watchlists', to='auctions.auction'),
        ),
    ]
