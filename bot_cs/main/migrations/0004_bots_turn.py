# Generated by Django 3.1.6 on 2021-03-28 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='bots',
            name='turn',
            field=models.BooleanField(default=False),
        ),
    ]
