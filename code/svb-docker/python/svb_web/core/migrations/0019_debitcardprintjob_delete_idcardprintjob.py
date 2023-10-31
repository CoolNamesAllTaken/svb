# Generated by Django 4.2.6 on 2023-10-31 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_bankstate_customer_referral_reward_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebitCardPrintJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('debit_card_pdf_path', models.CharField()),
            ],
        ),
        migrations.DeleteModel(
            name='IdCardPrintJob',
        ),
    ]
