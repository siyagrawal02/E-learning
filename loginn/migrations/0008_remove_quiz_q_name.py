# Generated by Django 4.1b1 on 2023-03-18 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0007_alter_quiz_q_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='q_name',
        ),
    ]