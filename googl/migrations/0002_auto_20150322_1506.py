# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='true_url',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
