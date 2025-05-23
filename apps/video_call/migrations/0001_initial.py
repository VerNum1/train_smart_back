# Generated by Django 5.2.1 on 2025-05-19 10:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('ONGOING', 'Активен'), ('ENDED', 'Завершен')], max_length=10)),
                ('call_type', models.CharField(choices=[('PRIVATE', 'Личный'), ('GROUP', 'Групповой')], max_length=10)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_calls', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_calls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
