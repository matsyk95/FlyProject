# Generated by Django 2.1.2 on 2019-04-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly', '0023_auto_20190412_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fly',
            name='descinationplace',
            field=models.CharField(max_length=40),
        ),
    ]
