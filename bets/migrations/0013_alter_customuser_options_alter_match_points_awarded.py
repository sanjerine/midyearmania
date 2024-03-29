# Generated by Django 4.0.5 on 2022-06-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0012_alter_customuser_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-points']},
        ),
        migrations.AlterField(
            model_name='match',
            name='points_awarded',
            field=models.CharField(default='', help_text='Int array of length 2, string separated by commas', max_length=500),
        ),
    ]
