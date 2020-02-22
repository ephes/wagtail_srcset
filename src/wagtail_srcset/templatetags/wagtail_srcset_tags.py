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
    wagtail image tag filter specs, although it wouldn't make much
    sence to use fill-80x80 or scale-50 inside srcset. At the moment
    width and jpegquality are the only supported operations.
    """
    ALLOWED_OPERATIONS = {"width", "jpegquality"}
    DEFAULT_WIDTHS = (2200, 1100, 768, 500, 300)
    DEFAULT_SRCSET_RENDITIONS = [f"width-{dw}" for dw in DEFAULT_WIDTHS]

    def __init__(self, image_node):
        self.image_node = image_node
        # need to set this inside __init__
        self.srcset_attribute = self.image_node.attrs.get("srcset", None)

    def get_allowed_operations(self, filter_spec):
        operations = []
        used_operations = set()
        for operation in filter_spec.split("|"):
            name = operation.split("-")[0]
            already_used = name in used_operations
            operation_allowed = name in self.ALLOWED_OPERATIONS
            if operation_allowed and not already_used:
                operations.append(operation)
                used_operations.add(name)
        return operations, used_operations

    def filter_specs_from_srcset(self, srcset):
        srcset = srcset.strip('"').strip("'")
        return srcset.split(" ")

    def merge_filter_specs(self, srcset_filter_specs, operations_from_tag):
        filter_specs = []
        for filter_spec in srcset_filter_specs:
            operations, used = self.get_allowed_operations(filter_spec)
            # inherit operations from tag if allowed and not already used
            # by the srcset attribute
            for operation in operations_from_tag:
                if operation not in used:
                    operations.append(operation)
            filter_specs.append("|".join(operations))
        return filter_specs

    def get_srcset_filter_specs(self, image):
        if self.srcset_attribute is not None:
            return self.filter_specs_from_srcset(self.srcset_attribute.token)
        if hasattr(settings, "DEFAULT_SRCSET_RENDITIONS"):
            return settings.DEFAULT_SRCSET_RENDITIONS
        return self.DEFAULT_SRCSET_RENDITIONS

    def get_merged_filter_specs(self, image):
        srcset_filter_specs = self.get_srcset_filter_specs(image)
        operations_from_tag, _ = self.get_allowed_operations(self.image_node.filter_spec)
        return self.merge_filter_specs(srcset_filter_specs, operations_from_tag)

    def resolve(self, context):
        image = self.image_node.image_expr.resolve(context)
        out_renditions = []
        for filter_spec in self.get_merged_filter_specs(image):
            rendered_image = image.get_rendition(filter_spec)
            out_renditions.append(f"{rendered_image.url} {rendered_image.width}w")
        srcset_string = ", ".join(out_renditions)
        return srcset_string
