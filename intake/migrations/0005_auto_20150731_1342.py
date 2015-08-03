# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('intake', '0004_callaudititem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='call',
            name='is_duplicate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='call',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='callassignment',
            name='call',
            field=models.ForeignKey(to='intake.Call'),
        ),
        migrations.AddField(
            model_name='callassignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
