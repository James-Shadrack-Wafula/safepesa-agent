# Generated by Django 3.2.18 on 2023-10-14 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transacted_amount',
            field=models.IntegerField(default=0),
        ),
    ]