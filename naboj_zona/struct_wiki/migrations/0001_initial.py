# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-20 14:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='struct_wiki.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('member', 'Member'), ('admin', 'Admin'), ('viewer', 'Viewer')], max_length=8)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='struct_wiki.Domain')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'domain')]),
        ),
        migrations.CreateModel(
            name='ArticleHolder',
            fields=[
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='holder', to='wiki.Article')),
                ('recursive', models.BooleanField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_holders', to='struct_wiki.Domain')),
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='domain',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='articleholder',
            name='tags',
            field=models.ManyToManyField(related_name='articles', to='struct_wiki.ArticleTag'),
        ),
    ]
