# Generated by Django 4.0.4 on 2022-05-23 01:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0013_alter_pricehistoricmodel_time_saved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storemodel',
            options={'verbose_name': 'store', 'verbose_name_plural': 'stores'},
        ),
        migrations.AlterField(
            model_name='storemodel',
            name='link',
            field=models.URLField(
                default='https://<django.db.models.fields.CharField>.com/',
                unique=True),
        ),
    ]
