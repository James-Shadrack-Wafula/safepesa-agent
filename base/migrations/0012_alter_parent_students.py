# Generated by Django 4.2.7 on 2023-11-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_parent_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='students',
            field=models.ManyToManyField(related_name='parents', to='base.student'),
        ),
    ]