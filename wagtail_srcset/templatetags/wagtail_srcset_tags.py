import types

from django import template
from django.conf import settings
from wagtail.images.templatetags.wagtailimages_tags import image as image_tag

register = template.Library()


def monkeypatch_wagtail_as_syntax(image_node):
    """
    If you use wagtails 'as' syntax like this:

    {% srcset_image photo width-300 as thumbnail %}

    image_node["attrs"] are not resolved. This patch resolves
    srcset and attaches it to the returned rendition. It's a
    bit hacky but should work.
    """

    def render_patched(self, context):
        result = self._original_render(context)
        if self.output_var_name:
            rendition = context[self.output_var_name]
            rendition.srcset = self.attrs["srcset"].resolve(context)
            rendition.original = self.attrs["srcset"].original_url
        return result

    image_node._original_render = image_node.render
    image_node.render = types.MethodType(render_patched, image_node)
    return image_node


@register.tag(name="srcset_image")
def srcset_image(parser, token):
    image_node = image_tag(parser, token)
    image_node.attrs["srcset"] = SrcSet(image_node)
    image_node = monkeypatch_wagtail_as_syntax(image_node)
    return image_node


class SrcSet:
    """
    Sets the srcset attribute of an image. You can either set it
    explicitly like this:

    {% srcset_image img width-600 srcset="width-1200 width-300" %}

    Or leave it out and let it be set automatically:

    {% srcset_image img width-600 %}

    Entries in the srcset attribute have the same syntax as normal
    wagtail image tag filter specs, although it wouldn't make much
    sense to use fill-80x80 or scale-50 inside srcset. At the moment
    width and jpegquality are the only supported operations.
    """

    ALLOWED_OPERATIONS = {"width", "jpegquality"}
    DEFAULT_WIDTHS = (2200, 1100, 768, 500, 300)
    DEFAULT_SRCSET_RENDITIONS = [f"width-{dw}" for dw in DEFAULT_WIDTHS]

    def __init__(self, image_node):
        self.image_node = image_node
        # need to set this inside __init__
        self.srcset_attribute = self.image_node.attrs.get("srcset", None)
        self.resolved_image = None

    def get_allowed_operations(self, filter_specs):
        """
        Gets a list of filter_specs and returns a list of allowed
        operations from this list and a set of used operations.
        """
        operations = []
        used_operations = set()
        for operation in filter_specs:
            name = operation.split("-")[0]
            already_used = name in used_operations
            operation_allowed = name in self.ALLOWED_OPERATIONS
            if operation_allowed and not already_used:
                operations.append(operation)
                used_operations.add(name)
        return operations, used_operations

    @staticmethod
    def filter_specs_from_srcset(srcset):
        srcset = srcset.strip('"').strip("'")
        return srcset.split(" ")

    def merge_filter_specs(self, srcset_filter_specs, operations_from_tag):
        """
        Merges the filter specs from the srcset attribute with the
        operations from the tag.
        """
        filter_specs = []
        for filter_spec in srcset_filter_specs:
            operations, used = self.get_allowed_operations(filter_spec.split("|"))
            # inherit operations from tag if allowed and not already used
            # by the srcset attribute
            for operation in operations_from_tag:
                name = operation.split("-")[0]
                if name not in used:
                    operations.append(operation)
            filter_specs.append("|".join(operations))
        return filter_specs

    def get_default_scale_factors(self):
        max_width = max(self.DEFAULT_WIDTHS)
        return [dw / max_width for dw in self.DEFAULT_WIDTHS]

    def get_maximum_width(self, image):
        max_useful_width = image.width
        for operation in self.image_node.filter_spec.split("|"):
            name, rest = operation.split("-")
            if name == "width" and len(rest) > 0:
                # if width-300 is set, there's no point serving
                # a 2800px image - limit to 900px instead
                max_useful_width = int(rest) * 3
        return min(image.width, max_useful_width)

    def calc_filter_specs(self, image):
        max_width = self.get_maximum_width(image)
        filter_specs = []
        for scale in self.get_default_scale_factors():
            width = int(scale * max_width)
            filter_specs.append(f"width-{width}")
        return filter_specs

    def get_srcset_filter_specs(self, image):
        """
        Returns the filter specs that should be used for the srcset.
          - If the srcset attribute is set, use that
          - Otherwise, use the DEFAULT_SRCSET_RENDITIONS setting if set
          - Otherwise, calculate the renditions based on the image
          - Otherwise, use the DEFAULT_WIDTHS setting
        """
        if self.srcset_attribute is not None:
            return self.filter_specs_from_srcset(self.srcset_attribute.token)
        if hasattr(settings, "DEFAULT_SRCSET_RENDITIONS"):
            return settings.DEFAULT_SRCSET_RENDITIONS
        if getattr(settings, "SRCSET_DYNAMIC", False):
            return self.calc_filter_specs(image)
        return self.DEFAULT_SRCSET_RENDITIONS

    @property
    def image_node_filter_specs(self):
        """
        Wagtail 5.0 changed the way filter specs are stored on the image node
        from a string to a list.
        """
        if hasattr(self.image_node, "filter_specs"):
            return self.image_node.filter_specs
        else:
            return self.image_node.filter_spec.split("|")

    def get_merged_filter_specs(self, image):
        """
        Merge the filter specs from the srcset attribute and the filter_specs
        set on the image node which is passed into this method.
        """
        srcset_filter_specs = self.get_srcset_filter_specs(image)
        image_node_filter_specs = self.image_node_filter_specs
        # filter operations from tag that should be used in srcset, too
        operations_from_tag, _ = self.get_allowed_operations(image_node_filter_specs)
        return self.merge_filter_specs(srcset_filter_specs, operations_from_tag)

    def resolve(self, context):
        """
        Resolve the image node and return a srcset string.
        """
        self.resolved_image = image = self.image_node.image_expr.resolve(context)
        out_renditions = []
        # create out_renditions from filter specs
        for filter_spec in self.get_merged_filter_specs(image):
            rendered_image = image.get_rendition(filter_spec)
            out_renditions.append(f"{rendered_image.url} {rendered_image.width}w")
        # create a srcset string from out_renditions
        srcset_string = ", ".join(out_renditions)
        return srcset_string

    @property
    def original_url(self):
        return self.resolved_image.file.url
