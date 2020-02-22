import pytest

from django.template import Context
from django.template.base import Template

from wagtail_srcset.templatetags.wagtail_srcset_tags import SrcSet

from .utils import extract_srcset_from_image_tag


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


class TestEmptySrcSetAttribute:
    pytestmark = pytest.mark.django_db

    def test_srcset_image_tag(self, rendered_result):
        assert "srcset" in rendered_result

    def test_default_renditions(self, rendered_srcset):
        for dw in SrcSet.DEFAULT_WIDTHS:
            assert str(dw) in rendered_srcset

    def test_settings_default_renditions(self, srcset_template, image, settings):
        t = Template(srcset_template)
        width = "537"
        settings.DEFAULT_SRCSET_RENDITIONS = [f"width-{width}"]
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert width in srcset


class TestSrcSetImageTag:
    pytestmark = pytest.mark.django_db

    def test_srcset_image_with_alt(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 alt="some description" %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        assert 'alt="some description"' in result

    def test_empty_srcset_inherits_jpegquality_from_tag(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 jpegquality-90%}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert "jpegquality-90" in srcset

    def test_srcset_operation_doesnt_get_overwritten(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 jpegquality-90 srcset="width-600|jpegquality-40" %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert "jpegquality-40" in srcset

    def test_use_first_operation(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 jpegquality-90 jpegquality-80 %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        assert "jpegquality-90" in srcset
        assert "jpegquality-80" not in srcset

    def test_srcset_use_first_operation(self, image):
        template_text = """
            {% load wagtail_srcset_tags %}
            {% srcset_image photo width-300 srcset="width-600|jpegquality-40|jpegquality-30" %}
        """
        t = Template(template_text)
        result = t.render(Context({"photo": image}))
        srcset = extract_srcset_from_image_tag(result)
        print(srcset)
        assert "jpegquality-40" in srcset
        assert "jpegquality-30" not in srcset
