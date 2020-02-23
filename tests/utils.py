import re


def extract_srcset_from_image_tag(tag):
    return re.search(r'srcset="(?P<srcset>.*?)"', tag).group("srcset")


class FakeImage:
    def __init__(self, width, filter_spec, attrs):
        self.width = width
        self.filter_spec = filter_spec
        self.attrs = attrs
