# Generated by Django 4.0.4 on 2022-05-17 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_contnet_reply_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='state',
            field=models.CharField(default='zero', max_length=40),
        ),
    ]
