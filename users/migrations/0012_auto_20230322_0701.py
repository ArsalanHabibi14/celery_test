# Generated by Django 3.2.11 on 2023-03-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20230322_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcodes',
            name='time',
            field=models.IntegerField(default=120, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='emailcodes',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
