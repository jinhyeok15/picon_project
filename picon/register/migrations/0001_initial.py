# Generated by Django 3.2.2 on 2021-05-29 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nick_name', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=16, null=True, unique=True)),
            ],
            options={
                'db_table': 'account',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_follow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_follow', to='register.account')),
                ('to_follow', models.ManyToManyField(related_name='to_follow', to='register.Account')),
            ],
            options={
                'db_table': 'follow',
            },
        ),
    ]