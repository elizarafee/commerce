# Generated by Django 3.1.3 on 2021-04-14 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_delete_closedlisting'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_winner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='auction_winner', to='auctions.bid')),
                ('closed_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='closed_listing', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
