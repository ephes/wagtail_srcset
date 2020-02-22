import re


def extract_srcset_from_image_tag(tag):
    return re.search(r'srcset="(?P<srcset>.*?)"', tag).group("srcset")
