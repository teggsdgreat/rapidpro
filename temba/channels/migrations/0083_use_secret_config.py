# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 16:30
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations
import json


# migrates to using `secret` config variable instead of `secret` field on Channel for FB, JN and JC channels
# migrates to using `secret` config variable instead of `channel_secret` config variable for LN channels
def use_secret_config(apps, schema_editor):
    Channel = apps.get_model('channels', 'Channel')

    # for each facebook, junebug and jiochat channel, move secret into config
    for ch in Channel.objects.filter(channel_type__in=['FB', 'JN', 'JC']):
        config = json.loads(ch.config)
        config['secret'] = ch.secret
        ch.config = json.dumps(config)
        ch.save(update_fields=['config'])

    # for each line channel, move to `secret` from `channel_secret`
    for ch in Channel.objects.filter(channel_type='LN'):
        config = json.loads(ch.config)
        config['secret'] = config['channel_secret']
        ch.config = json.dumps(config)
        ch.save(update_fields=['config'])


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0082_update-nexmo-bulk-senders-channel-config'),
    ]

    operations = [
        migrations.RunPython(use_secret_config)
    ]
