# Generated by Django 4.1b1 on 2023-03-22 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0014_java'),
    ]

    operations = [
        migrations.CreateModel(
            name='Js',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default='null', max_length=1000)),
            ],
        ),
    ]
