# Generated by Django 4.0.3 on 2022-04-08 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_techskills_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='password',
        ),
    ]
