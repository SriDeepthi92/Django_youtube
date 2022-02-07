
# core/views.py
from django import forms
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.encoding import smart_str
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from .models import CredentialsModel, GoogleOAuthCredential
from .forms import YoutubeUploadForm
from django.urls import reverse
from django.forms.models import model_to_dict
from google.oauth2 import credentials


from oauth2client.contrib import xsrfutil
import http.client as httplib
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import tempfile
from django.http import HttpResponse, HttpResponseBadRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

httplib2.RETRIES = 1


MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)


RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "C:\Dev\Django-work\django_api\django_api\client_secret.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/youtube.upload',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent')

class YouTubeForm(forms.Form):
    video = forms.FileField()


class AuthorizeView(View):


    def get_authenticated_service(*args):
      flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
        redirect_uri=request.build_absolute_uri(
            reverse(settings.GOOGLE_OAUTH2_CALLBACK_VIEW)))

      storage = Storage("%s-oauth2.json" % sys.argv[0])
      credentials = storage.get()
      if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)
        authorize_url = flow.step1_get_authorize_url()
        return redirect(authorize_url)
      return redirect('/upload/')

class Oauth2CallbackView(View):

    def get(self, request, *args, **kwargs):
        if not xsrfutil.validate_token(
                settings.SECRET_KEY, request.GET.get('state').encode(),
                request.user):
            return HttpResponseBadRequest()
        global flow
        credentials = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(
            GoogleAPIOauthInfo, 'id', request.user.id, 'credentials')
        storage.put(credentials)
        return redirect('/upload/')

class AuthCallbackView(View):
    def get(self,request,*args,**kwargs):
        state = request.GET.get('state')
        flow = Flow.from_client_secrets_file(settings.YT_JSON_FILE, scopes=scopes,state=state)
        flow.redirect_uri = request.build_absolute_uri(reverse('auth_callback'))
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        credential = flow.credentials

        try:
            GoogleOAuthCredential.objects.create(token=credential.token,refresh_token=credential.refresh_token,token_uri=credential.token_uri,client_id= credential.client_id,client_secret=credential.client_secret,scopes=credential.scopes)
        except Exception as e:
            pass

        return redirect('/')

class HomeView(FormView):
    template_name = 'home.html'
    form_class = YoutubeUploadForm

    def form_valid(self,form):
        file_name = form.cleaned_data['video'].temporary_file_path()
        print(file_name)
        credentials_dict = model_to_dict(GoogleOAuthCredential.objects.get(client_secret=settings.YT_CLIENT_SECRET))
        credential = credentials.Credentials(**credentials_dict)
        youtube = build('youtube', 'v3', credentials=credential)
        body = {
            'snippet': {
                'title': 'Video uploaded using django',
                'description': 'This video has been uploaded using Django and Youtube Data API.',
                'tags': 'django,api',
                'categoryId': '27'
            },
            'status': {
                'privacyStatus': 'unlisted'
            }
        }

        insert_request = youtube.videos().insert(part=','.join(body.keys()),body=body,media_body=MediaFileUpload(file_name, chunksize=-1, resumable=True))
        response = insert_request.execute()

        #return HttpResponse('<h1>Hooray! It worked!</h1>')
        return redirect('result/')

def result(request):
    return render(request, 'result.html')
