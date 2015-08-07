# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("INSERT INTO workflow_casestatus (name) VALUES ('Closed');"),
        migrations.RunSQL("INSERT INTO workflow_casestatus (name) VALUES ('Active');"),
    ]
