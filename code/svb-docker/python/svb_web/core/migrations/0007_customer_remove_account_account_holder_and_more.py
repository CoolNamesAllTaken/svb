# Generated by Django 4.2.6 on 2023-10-16 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_newsarticle_body_newsarticle_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(default='TBA', max_length=6, primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='Edween')),
                ('costume', models.CharField(default='Founder')),
                ('referrer_customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_holder',
        ),
        migrations.DeleteModel(
            name='AccountHolder',
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
    ]
