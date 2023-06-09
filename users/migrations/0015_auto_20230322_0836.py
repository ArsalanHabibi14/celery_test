# Generated by Django 3.2.11 on 2023-03-22 15:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_emailcodes_email_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcodes',
            name='expiry_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 15, 36, 27, 759124, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='emailcodes',
            name='email_code',
            field=models.IntegerField(default=444579, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
