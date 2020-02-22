import re
import pytest

from django.template import Context
from django.template.base import Template

from wagtail_srcset.templatetags.wagtail_srcset_tags import SrcSet


def extract_srcset_from_image_tag(tag):
    return re.search(r'srcset="(?P<srcset>.*?)"', tag).group("srcset")


class TestWagtailImageTag:
    pytestmark = pytest.mark.django_db

    def test_default_wagtail_image_tag(self, image):
        template_text = """
            {% load wagtailimages_tags %}
            {% image photo width-300 %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        assert "img alt" in result


class TestSrcSetImageTag:
    pytestmark = pytest.mark.django_db

    def test_srcset_image_tag(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        assert "srcset" in result

    def test_srcset_image_with_alt(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 alt="some description" %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        assert 'alt="some description"' in result

    def test_empty_srcset_default(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        for dw in SrcSet.DEFAULT_WIDTHS:
            assert str(dw) in srcset

    def test_empty_srcset_inherits_jpegquality_from_tag(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 jpegquality-90%}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert "jpegquality-90" in srcset

    def test_empty_srcset_inherits_jpegquality_from_tag_but_dont_overwrite(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 jpegquality-90 srcset="width-600|jpegquality-40 width-300" %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert "jpegquality-40" in srcset
        assert "jpegquality-90" in srcset

    def test_empty_srcset_with_settings(self, image, settings):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 %}
        """
        t = Template(template_text)
        width = "537"
        settings.DEFAULT_SRCSET_RENDITIONS = [f"width-{width}"]
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert width in srcset
