# Generated by Django 4.0.4 on 2022-05-15 19:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_pricemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistoricModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('time_saved', models.DateField(default=datetime.date.today,
                                                unique_for_date=True)),
                ('game',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='core.gamemodel')),
            ],
            options={
                'verbose_name': 'price historic',
                'verbose_name_plural': 'prices historic',
            },
        ),
    ]
