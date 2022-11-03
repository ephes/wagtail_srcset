from django.views.generic import TemplateView
from wagtail.images.models import Image as WagtailImage


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["img"] = WagtailImage.objects.first()
        return context
