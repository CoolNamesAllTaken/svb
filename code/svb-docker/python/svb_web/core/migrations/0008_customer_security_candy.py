# Generated by Django 4.2.6 on 2023-10-19 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_customer_remove_account_account_holder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='security_candy',
            field=models.CharField(default=''),
        ),
    ]
