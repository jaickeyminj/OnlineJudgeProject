# Generated by Django 4.0.3 on 2022-04-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(default='Easy', max_length=10),
        ),
    ]
