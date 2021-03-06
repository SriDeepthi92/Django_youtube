from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    credential = CredentialsField()

class GoogleOAuthCredential(models.Model):
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField(primary_key=True)
    scopes = models.URLField(max_length=240)

    def __str__(self):
        return self.client_id
