# Generated by Django 4.0.5 on 2022-06-16 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('start_time', models.DateTimeField()),
                ('players', models.CharField(default='', help_text='Players list; string separated by commas', max_length=500)),
                ('points_awarded', models.CharField(default='', help_text='Players list; string separated by commas', max_length=500)),
                ('betpool_points', models.PositiveIntegerField(default=20)),
                ('winner', models.CharField(choices=[('MB', 'Mirabooka Bucks'), ('MH', 'Melville Heat'), ('NK', 'North Perth Knicks'), ('WW', 'Willetton Wizards')], default=None, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bets.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]