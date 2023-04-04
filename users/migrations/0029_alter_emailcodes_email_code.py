# Generated by Django 3.2.11 on 2023-03-31 05:16

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_emailcodes_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcodes',
            name='email_code',
            field=models.IntegerField(default=users.models.random_num, primary_key=True, serialize=False, unique=True),
        ),
    ]
