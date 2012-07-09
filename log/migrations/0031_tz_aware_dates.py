# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

import pytz

class Migration(DataMigration):

  def forwards(self, orm):
    old_tz = pytz.timezone(settings.TIME_ZONE)
    # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
    for news in orm['log.News'].objects.all():
      news.date = news.date.replace(tzinfo = old_tz).astimezone(pytz.utc)
      news.save()

    for comment in orm['log.Comment'].objects.all():
      comment.date = comment.date.replace(tzinfo = old_tz).astimezone(pytz.utc)
      comment.save()

    for log in orm['log.Log'].objects.all():
      log.last_update = log.last_update.replace(tzinfo = old_tz).astimezone(pytz.utc)
      log.save()

    for item in orm['log.LogItem'].objects.all():
      item.date = item.date.replace(tzinfo = old_tz).astimezone(pytz.utc)
      item.save()

    for user in orm['auth.User'].objects.all():
      user.date_joined = user.date_joined.replace(tzinfo = old_tz).astimezone(pytz.utc)
      user.last_login = user.last_login.replace(tzinfo = old_tz).astimezone(pytz.utc)
      user.save()

    for entry in orm['log.StatisticEntry'].objects.all():
      entry.date = entry.date.replace(tzinfo = old_tz).astimezone(pytz.utc)
      entry.save()

  def backwards(self, orm):
    "Write your backwards methods here."

  models = {
    'auth.group': {
        'Meta': {'object_name': 'Group'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
        'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
    },
    'auth.permission': {
        'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
        'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
    },
    'auth.user': {
        'Meta': {'object_name': 'User'},
        'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
        'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
        'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
        'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
        'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
        'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
        'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
        'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
        'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
    },
    'contenttypes.contenttype': {
        'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
        'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
    },
    'log.champion': {
        'Meta': {'ordering': "['name']", 'object_name': 'Champion'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'image': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
    },
    'log.comment': {
        'Meta': {'ordering': "['-date']", 'object_name': 'Comment'},
        'date': ('django.db.models.fields.DateTimeField', [], {}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['log.News']"}),
        'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
        'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
    },
    'log.locksite': {
        'Meta': {'object_name': 'LockSite'},
        'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'text': ('django.db.models.fields.TextField', [], {})
    },
    'log.log': {
        'Meta': {'ordering': "['-last_update']", 'object_name': 'Log'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'initial_elo': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
        'initial_games_left': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
        'initial_games_lost': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
        'initial_games_won': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
        'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'blank': 'True'}),
        'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        'public_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
        'region': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
        'show_on_public_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        'summoner_name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
        'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
    },
    'log.logcustomfield': {
        'Meta': {'ordering': "['order']", 'object_name': 'LogCustomField'},
        'display_on_overview': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['log.Log']"}),
        'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
        'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
        'type': ('django.db.models.fields.IntegerField', [], {})
    },
    'log.logcustomfieldvalue': {
        'Meta': {'object_name': 'LogCustomFieldValue'},
        '_value': ('django.db.models.fields.TextField', [], {'db_column': "'value'", 'blank': 'True'}),
        'custom_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['log.LogCustomField']"}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'log_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['log.LogItem']"})
    },
    'log.logitem': {
        'Meta': {'ordering': "['date']", 'object_name': 'LogItem'},
        'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['log.Log']"}),
        'outcome': ('django.db.models.fields.IntegerField', [], {'default': '0'})
    },
    'log.news': {
        'Meta': {'ordering': "['-date']", 'object_name': 'News'},
        'comments_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
        'date': ('django.db.models.fields.DateTimeField', [], {}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'text': ('django.db.models.fields.TextField', [], {}),
        'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
        'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
    },
    'log.statisticentry': {
        'Meta': {'ordering': "['-date']", 'object_name': 'StatisticEntry'},
        'active_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
        'date': ('django.db.models.fields.DateTimeField', [], {}),
        'game_count': ('django.db.models.fields.IntegerField', [], {}),
        'game_leave_count': ('django.db.models.fields.IntegerField', [], {}),
        'game_loss_count': ('django.db.models.fields.IntegerField', [], {}),
        'game_win_count': ('django.db.models.fields.IntegerField', [], {}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'log_count': ('django.db.models.fields.IntegerField', [], {}),
        'user_count': ('django.db.models.fields.IntegerField', [], {}),
        'users_online': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
        'wl_ratio': ('django.db.models.fields.FloatField', [], {})
    },
    'log.userprofile': {
        'Meta': {'object_name': 'UserProfile'},
        'date_format': ('django.db.models.fields.CharField', [], {'default': "'%d.%m.%Y'", 'max_length': '256'}),
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'last_activity': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
        'time_format': ('django.db.models.fields.CharField', [], {'default': "'%H:%M'", 'max_length': '256'}),
        'time_zone': ('django.db.models.fields.CharField', [], {'default': "'Europe/Vienna'", 'max_length': '256'}),
        'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
    }
  }

  complete_apps = ['log']
  symmetrical = True
