# Generated by Django 4.0.4 on 2022-05-11 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hyperdrated', '0002_rename_post_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='votes',
            field=models.ManyToManyField(blank=True, default=None, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=1)),
                ('blog_post', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='hyperdrated.blogpost')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
