from django import template
from django.conf import settings

from wagtail.images.templatetags.wagtailimages_tags import image


register = template.Library()


@register.tag(name="srcset_image")
def srcset_image(parser, token):
    image_node = image(parser, token)
    image_node.attrs["srcset"] = SrcSet(image_node)
    return image_node


class SrcSet:
    """
    Sets the srcset attribute of an image. You can either set it
    explicitly like this:

    {% srcset_image img width-600 srcset="width-1200 width-300" %}

    Entries in the srcset attribute have the same syntax as normal
    wagtail image tag resize-rule attributes, although it wouldn't
    make much sence to use fill-80x80 or scale-50 inside srcset.
    """
    DEFAULT_WIDTHS = (2200, 1100, 768, 500, 300)
    DEFAULT_SRCSET = [f"width-{dw}" for dw in DEFAULT_WIDTHS]

    def __init__(self, image_node):
        self.image_node = image_node
        srcset = image_node.attrs.get("srcset", None)
        if srcset is None:
            self.renditions = self.default_renditions
        else:
            self.renditions = self.renditions_from_srcset(srcset.token)

    @property
    def default_renditions(self):
        if hasattr(settings, "DEFAULT_SRCSET_RENDITIONS"):
            return settings.DEFAULT_SRCSET_RENDITIONS
        else:
            return self.DEFAULT_SRCSET

    def renditions_from_srcset(self, srcset):
        srcset = srcset.strip('"').strip("'")
        return srcset.split(" ")

    def resolve(self, context):
        image = self.image_node.image_expr.resolve(context)
        out_renditions = []
        for rendition in self.renditions:
            rendered_image = image.get_rendition(rendition)
            out_renditions.append(f"{rendered_image.url} {rendered_image.width}w")
        srcset_string = ", ".join(out_renditions)
        return srcset_string
