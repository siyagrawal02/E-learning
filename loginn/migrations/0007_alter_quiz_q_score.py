# Generated by Django 4.1b1 on 2023-03-18 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0006_alter_quiz_q_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='q_score',
            field=models.CharField(default='NUll', max_length=100),
        ),
    ]
