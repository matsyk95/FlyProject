# Generated by Django 2.1.2 on 2019-03-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly', '0012_auto_20190322_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fly',
            name='day',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='fly',
            name='month',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
