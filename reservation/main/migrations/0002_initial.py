# Generated by Django 5.2 on 2025-04-15 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='main.reservation'),
        ),
        migrations.AddField(
            model_name='seat',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='main.cinemahall'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.seat'),
        ),
        migrations.AddField(
            model_name='showtime',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_times', to='main.cinemahall'),
        ),
        migrations.AddField(
            model_name='showtime',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_times', to='main.movie'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='show_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.showtime'),
        ),
    ]
