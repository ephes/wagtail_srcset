from django.urls import include, path

urlpatterns = [
    path("", include("wagtail_srcset.urls", namespace="wagtail_srcset")),
]
