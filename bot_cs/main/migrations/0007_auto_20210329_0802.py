# Generated by Django 3.1.6 on 2021-03-29 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210329_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='max_profit',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='max_time',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='min_profit',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='min_time',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='place',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='s_time',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='steam',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
