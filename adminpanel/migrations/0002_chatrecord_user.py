# Generated by Django 4.2.2 on 2025-06-09 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatrecord',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_records', to=settings.AUTH_USER_MODEL),
        ),
    ]
