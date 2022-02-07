# core/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import AuthorizeView, HomePageView, Oauth2CallbackView

urlpatterns = [
    #path('video/', HomePageView.as_view(), name='video'),
    #path('authorize/', AuthorizeView.as_view(), name='authorize'),
    #path('oauth2callback/', Oauth2CallbackView.as_view(),
         #name='oauth2callback'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
