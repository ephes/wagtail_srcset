from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from .views import MainView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("manual/", TemplateView.as_view(template_name="manual.html"), name="manual"),
    path("thumbnails/", MainView.as_view(template_name="thumbnails.html"), name="thumbnails"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
