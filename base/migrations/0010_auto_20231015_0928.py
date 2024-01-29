# Generated by Django 3.2.18 on 2023-10-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20231014_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('parents_code', models.CharField(blank=True, max_length=200, null=True)),
                ('students', models.ManyToManyField(to='base.Student')),
            ],
        ),
    ]