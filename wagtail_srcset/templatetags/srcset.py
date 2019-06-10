from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def srcset(image, *args):
    """
    Generate an image tag with a srcset for a given image.

    :param image: The image field you want to render
    :param args: If you want to specify renditions, put them here, otherwise the standard renditions will be generated
    """

    renditions = args
    if renditions is None:
        renditions = settings.STANDARD_RENDITIONS      # TODO: actual setting

    out_renditions = []

    for rendition in renditions:
        rendered_image = image.get_rendition(rendition)
        out_renditions.append(f"{rendered_image.url} {rendered_image.width}w")

    return f"""srcset="{",".join(out_renditions)}" """




