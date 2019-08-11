import pytest

from django.template import Context
from django.template.base import Template


from wagtail_srcset.templatetags.wagtail_srcset_tags import srcset_image as image_tag


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
