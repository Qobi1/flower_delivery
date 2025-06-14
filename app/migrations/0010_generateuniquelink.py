# Generated by Django 5.2.1 on 2025-06-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_approvedby_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateUniqueLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=128, unique=True)),
                ('total_visit', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Уникальная ссылка',
                'verbose_name_plural': 'Уникальная ссылка',
            },
        ),
    ]
