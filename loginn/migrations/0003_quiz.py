# Generated by Django 4.1b1 on 2023-03-18 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0002_user_firstname_user_lastname_alter_user_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_name', models.CharField(default='NULL', max_length=100)),
                ('q_score', models.IntegerField(default='Null')),
                ('q_time', models.CharField(default='NUll', max_length=100)),
            ],
        ),
    ]
