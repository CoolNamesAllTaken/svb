# Generated by Django 4.2.6 on 2023-10-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_customer_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(default='TBA', max_length=12, primary_key=True, serialize=False),
        ),
    ]
