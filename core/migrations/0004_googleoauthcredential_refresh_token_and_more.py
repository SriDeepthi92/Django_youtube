# Generated by Django 4.0.2 on 2022-02-06 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_googleoauthcredential_refresh_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='googleoauthcredential',
            name='refresh_token',
            field=models.TextField(default='1//04W2VUwgJD1UqCgYIARAAGAQSNwF-L9Irs28DX5JMp2qkjuyzv9DzrO63itI2tQtMSFDSxS1l0NNzKvQey6dZvBUwF-QckVhTBX4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googleoauthcredential',
            name='token',
            field=models.TextField(default='ya29.A0ARrdaM9XeoPgNmbIuau1LnFdCUaX6ewWqBhHlOfCmQv68fVvIyfZZAPLWcKqtsf183omwQWVSRzlxjjAeGIhj4ApUrgMWsq-Y5JbUvFuFL8DlK8CCuUa6iQn_OHoI3-XfxK4qifXjjFq6NJnVIVaiqVpH9vt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googleoauthcredential',
            name='token_uri',
            field=models.TextField(default='https://accounts.google.com/o/oauth2/token'),
            preserve_default=False,
        ),
    ]
