# Generated by Django 4.2.6 on 2023-10-30 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_bankstate_newsarticle_eek_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankstate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
