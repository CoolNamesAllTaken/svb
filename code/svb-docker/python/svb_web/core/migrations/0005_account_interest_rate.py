# Generated by Django 4.2.6 on 2023-10-14 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_newsarticle_date_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='interest_rate',
            field=models.FloatField(default=0.0),
        ),
    ]
