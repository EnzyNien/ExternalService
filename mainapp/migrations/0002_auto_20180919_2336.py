# Generated by Django 2.0.4 on 2018-09-19 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_lat', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='latitude')),
                ('geo_lng', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='longitude')),
                ('full_name', models.CharField(blank=True, max_length=250, verbose_name='full_name')),
            ],
            options={
                'verbose_name': 'Adress item',
                'verbose_name_plural': 'Adresses items',
            },
        ),
        migrations.RemoveField(
            model_name='adress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='adress',
            name='street',
        ),
        migrations.RemoveField(
            model_name='adress',
            name='suite',
        ),
        migrations.RemoveField(
            model_name='adress',
            name='zipcode',
        ),
        migrations.AlterModelOptions(
            name='classifier',
            options={'ordering': ['typeof'], 'verbose_name': 'Adress Classifier', 'verbose_name_plural': 'Adresses Classifiers'},
        ),
        migrations.AddField(
            model_name='companys',
            name='on_load',
            field=models.BooleanField(default=False, verbose_name='load form json'),
        ),
        migrations.AddField(
            model_name='units',
            name='on_load',
            field=models.BooleanField(default=False, verbose_name='load form json'),
        ),
        migrations.AlterField(
            model_name='classifier',
            name='typeof',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'zipcode'), (1, 'region'), (2, 'city'), (3, 'street'), (4, 'suite')], null=True, verbose_name='adress type'),
        ),
        migrations.AlterField(
            model_name='companys',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CompanyAdress', to='mainapp.Address'),
        ),
        migrations.AlterField(
            model_name='units',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mainapp.Address'),
        ),
        migrations.AlterField(
            model_name='units',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mainapp.Companys'),
        ),
        migrations.AlterField(
            model_name='units',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Phone'),
        ),
        migrations.DeleteModel(
            name='Adress',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='region_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='street_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='address',
            name='suite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suite_set', to='mainapp.Classifier'),
        ),
        migrations.AddField(
            model_name='address',
            name='zipcode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zipcode_set', to='mainapp.Classifier'),
        ),
    ]
