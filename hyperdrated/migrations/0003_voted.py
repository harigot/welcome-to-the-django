# Generated by Django 4.0.4 on 2022-05-11 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hyperdrated', '0002_rename_post_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(choices=[(0, 'nope'), (1, 'yep')], default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hyperdrated.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]