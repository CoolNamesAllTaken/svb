# Generated by Django 4.2.6 on 2023-10-12 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsauthor',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
