# Generated by Django 3.2.11 on 2023-03-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_emailcodes_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcodes',
            name='email_code',
            field=models.IntegerField(default=212530, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
