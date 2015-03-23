# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googl', '0002_auto_20150322_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='true_url',
            field=models.CharField(default=b'not found', max_length=200),
            preserve_default=True,
        ),
    ]
