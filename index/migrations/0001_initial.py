# Generated by Django 4.0.4 on 2022-05-19 18:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('slug', models.CharField(max_length=256)),
                ('pages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), size=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('language', models.CharField(max_length=2)),
                ('slug', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=8196)),
                ('thumbnail', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_draft', models.BooleanField(default=False)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), size=None)),
                ('chapters', models.ManyToManyField(to='index.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('thumbnail', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=256)),
                ('language', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.chapter')),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.manga')),
            ],
        ),
    ]
