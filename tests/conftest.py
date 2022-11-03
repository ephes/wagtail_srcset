import io
import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context
from django.template.base import Template
from PIL import Image
from wagtail.images.models import Image as WagtailImage

from .utils import extract_srcset_from_image_tag


def create_small_rgb():
    # this is a small test jpeg
    img = Image.new("RGB", (200, 200), (255, 0, 0, 0))
    return img


@pytest.fixture()
def small_jpeg_io():
    rgb = create_small_rgb()
    im_io = io.BytesIO()
    rgb.save(im_io, format="JPEG", quality=60, optimize=True, progressive=True)
    im_io.seek(0)
    im_io.name = "testimage.jpg"
    return im_io


@pytest.fixture()
def small_uploaded_file(small_jpeg_io):
    simple_png = SimpleUploadedFile(
        name="test.png", content=small_jpeg_io.read(), content_type="image/png"
    )
    small_jpeg_io.seek(0)
    return simple_png


@pytest.fixture()
def image(small_uploaded_file):
    image = WagtailImage(file=small_uploaded_file)
    image.save()
    yield image
    # teardown
    os.unlink(image.file.path)


@pytest.fixture()
def srcset_template():
    return """
        {% load wagtail_srcset_tags %}
        {% srcset_image photo width-300 %}
    """


@pytest.fixture()
def rendered_result(srcset_template, image):
    t = Template(srcset_template)
    return t.render(Context({"photo": image}))


@pytest.fixture()
def rendered_srcset(rendered_result):
    return extract_srcset_from_image_tag(rendered_result)
