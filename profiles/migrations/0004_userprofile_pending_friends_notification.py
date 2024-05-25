# Generated by Django 5.0.3 on 2024-05-25 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userprofile_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pending_friends',
            field=models.ManyToManyField(blank=True, to='profiles.userprofile'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bootstrap_icon', models.TextField()),
                ('notification_text', models.TextField()),
                ('hyperlink', models.TextField(blank=True)),
                ('notify_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile')),
            ],
        ),
    ]
