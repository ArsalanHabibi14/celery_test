# Generated by Django 3.2.11 on 2023-03-22 03:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230315_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 22, 3, 25, 37, 315805, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='companytoken',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 22, 3, 25, 37, 315805, tzinfo=utc), null=True),
        ),
    ]
