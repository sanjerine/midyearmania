# Generated by Django 4.0.5 on 2022-06-16 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0004_alter_match_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='players',
        ),
        migrations.AlterField(
            model_name='match',
            name='points_awarded',
            field=models.CharField(default='', help_text='Int array of length 2 or 4, string separated by commas', max_length=500),
        ),
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(related_name='teams', to='bets.team'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bets.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='winner', to='bets.team'),
        ),
    ]
