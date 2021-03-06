# Generated by Django 2.1 on 2018-09-19 12:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mainapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_lat', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='latitude')),
                ('geo_lng', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='longitude')),
            ],
            options={
                'verbose_name': 'Adress item',
                'verbose_name_plural': 'Adress items',
            },
        ),
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('typeof', models.PositiveIntegerField(blank=True, choices=[(0, 'zipcode'), (1, 'city'), (2, 'street'), (3, 'suite')], null=True, verbose_name='adress type')),
            ],
            options={
                'verbose_name': 'Adress part',
                'verbose_name_plural': 'Adress parts',
                'ordering': ['typeof'],
            },
            bases=(models.Model, mainapp.models.GetTypeChoices),
        ),
        migrations.CreateModel(
            name='Companys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Company')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Adress', verbose_name='Adress')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companys',
            },
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{11}$')], verbose_name='Phone')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Adress', verbose_name='Adress')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Companys', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.AddField(
            model_name='adress',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='adress',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='street_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='adress',
            name='suite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='adress',
            name='zipcode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zipcode_set', to='mainapp.Classifier'),
        ),
    ]
