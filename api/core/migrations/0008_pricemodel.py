# Generated by Django 4.0.4 on 2022-05-15 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_storemodel_remove_gamemodel_epic_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('game',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='core.gamemodel')),
                ('store',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='core.storemodel')),
            ],
            options={
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
            },
        ),
    ]
