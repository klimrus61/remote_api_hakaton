# Generated by Django 4.1 on 2022-11-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]