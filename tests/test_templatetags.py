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
