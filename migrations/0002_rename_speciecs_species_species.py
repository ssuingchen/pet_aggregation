# Generated by Django 3.2 on 2021-04-22 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='species',
            old_name='speciecs',
            new_name='species',
        ),
    ]
