# Generated by Django 2.1.2 on 2019-03-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly', '0021_auto_20190329_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='fly',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fly',
            name='descinationplace',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
