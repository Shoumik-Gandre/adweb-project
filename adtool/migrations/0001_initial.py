# Generated by Django 3.0.4 on 2020-05-18 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images/')),
                ('url_link', models.URLField(default='')),
                ('clicks', models.IntegerField(default=0)),
                ('category', models.IntegerField(choices=[(0, 'science'), (1, 'math'), (2, 'anime'), (3, 'computers'), (4, 'nature'), (5, 'news'), (6, 'music'), (7, 'politics'), (8, 'anthology'), (9, 'medical'), (10, 'sports'), (11, 'others')], default='others')),
                ('size', models.CharField(choices=[('medium rectangle', '300x250 pixels'), ('large rectangle', '336x280 pixels'), ('leaderboard', '728x90 pixels'), ('half page', '320x600 pixels'), ('free size', 'free size')], default='free size', max_length=16)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('is_enabled', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('userkey', models.CharField(default='0', max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date clicked')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adtool.Advertisement')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adtool.Website')),
            ],
        ),
    ]
