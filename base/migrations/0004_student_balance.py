# Generated by Django 3.2.18 on 2023-10-10 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_student_student_adm'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='balance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
