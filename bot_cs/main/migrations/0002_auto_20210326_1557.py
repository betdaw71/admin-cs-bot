# Generated by Django 3.1.6 on 2021-03-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bots',
            name='steamid',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
