# Generated by Django 3.2.11 on 2023-03-29 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_emailcodes_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcodes',
            name='email_code',
            field=models.IntegerField(default=400883, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
