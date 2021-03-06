# Generated by Django 3.2.2 on 2021-07-17 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='heart', max_length=10)),
                ('status', models.SmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_feed_back', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_feed_back', to='register.account')),
                ('to_feed_back', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_feed_back', to='register.account')),
            ],
        ),
    ]
