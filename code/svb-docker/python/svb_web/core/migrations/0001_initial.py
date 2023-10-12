# Generated by Django 4.2.6 on 2023-10-12 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdCardPrintJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NewsAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=128)),
                ('date_published', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.newsauthor')),
            ],
        ),
        migrations.CreateModel(
            name='AccountHolder',
            fields=[
                ('account_holder_number', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='Edween')),
                ('costume', models.CharField(default='Founder')),
                ('referrer_account_holder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.accountholder')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_number', models.AutoField(primary_key=True, serialize=False)),
                ('last_anchor_event_timestamp', models.DateTimeField(auto_now=True)),
                ('last_anchor_event_balance', models.DecimalField(decimal_places=3, max_digits=10)),
                ('account_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.accountholder')),
            ],
        ),
    ]
