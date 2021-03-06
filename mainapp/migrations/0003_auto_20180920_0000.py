# Generated by Django 2.0.4 on 2018-09-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20180919_2336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address item', 'verbose_name_plural': 'Addresses items'},
        ),
        migrations.AlterModelOptions(
            name='classifier',
            options={'ordering': ['typeof'], 'verbose_name': 'Address Classifier', 'verbose_name_plural': 'Addresses Classifiers'},
        ),
        migrations.RenameField(
            model_name='address',
            old_name='geo_lat',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='geo_lng',
            new_name='lng',
        ),
        migrations.AlterField(
            model_name='classifier',
            name='typeof',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'zipcode'), (1, 'region'), (2, 'city'), (3, 'street'), (4, 'suite')], null=True, verbose_name='address type'),
        ),
    ]
