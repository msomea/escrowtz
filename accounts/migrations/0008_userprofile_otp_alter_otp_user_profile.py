# Generated by Django 5.0.6 on 2024-06-18 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_rename_otp_code_otp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='otp',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_set', to='accounts.userprofile'),
        ),
    ]
