# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import MainView


urlpatterns = [
    url(r"^$", MainView.as_view(), name="main"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
