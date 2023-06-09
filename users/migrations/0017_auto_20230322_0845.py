# Generated by Django 3.2.11 on 2023-03-22 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20230322_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcodes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='emailcodes',
            name='email_code',
            field=models.IntegerField(default=524468, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
