# Generated by Django 4.1.4 on 2023-01-28 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newproject', '0009_rename_user_profile_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]
