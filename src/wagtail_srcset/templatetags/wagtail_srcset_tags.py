from django import template
from django.conf import settings

from wagtail.images.templatetags.wagtailimages_tags import image


register = template.Library()


@register.tag(name="srcset_image")
def srcset_image(parser, token):
    image_node = image(parser, token)
    print(image_node)
    print(dir(image_node))
    image_node.attrs["srcset"] = SrcSet(image_node)
    return image_node


class SrcSet:
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
            return [
                "width-2200|jpegquality-60",
                "width-1100|jpegquality-60",
                "width-768|jpegquality-60",
                "width-500|jpegquality-60",
                "width-300|jpegquality-60",
            ]

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
