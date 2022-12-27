# Generated by Django 4.1.4 on 2022-12-27 08:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserdata',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 27, 9, 49, 44, 50829)),
        ),
        migrations.AlterField(
            model_name='additionaluserdata',
            name='date_registred',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 27, 9, 49, 44, 50829)),
        ),
        migrations.AlterField(
            model_name='additionaluserdata',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 27, 9, 49, 44, 50829)),
        ),
        migrations.AlterField(
            model_name='gender',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 27, 9, 49, 44, 50829)),
        ),
        migrations.AlterField(
            model_name='roles',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
