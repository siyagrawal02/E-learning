# Generated by Django 4.1b1 on 2023-03-19 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0010_note'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
    ]