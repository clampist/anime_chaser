# Generated by Django 2.2.2 on 2019-07-05 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]