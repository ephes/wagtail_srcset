=============================
wagtail-srcset
=============================

.. image:: https://badge.fury.io/py/wagtail-srcset.svg
    :target: https://badge.fury.io/py/wagtail-srcset

.. image:: https://img.shields.io/badge/python-3.9%7C3.10%7C3.11-brightgreen
    :target: https://img.shields.io/badge/python-3.9%7C3.10%7C3.11-brightgreen

.. image:: https://img.shields.io/badge/wagtail-3%7C4%7C5-brightgreen
    :target: https://img.shields.io/badge/wagtail-3%7C4%7C5-brightgreen

.. image:: https://codecov.io/gh/ephes/wagtail_srcset/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/ephes/wagtail_srcset

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ephes/wagtail-srcset

HTML5 image srcset support for Wagtail

Quickstart
----------

Install wagtail-srcset::

    pip install wagtail-srcset

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "wagtail_srcset.apps.WagtailSrcsetConfig",
        ...
    )

Use it in your templates:

.. code-block:: python

    {% load wagtail_srcset_tags %}
    {% srcset_image img width-600 %}

Or via wagtails "as" syntax:

.. code-block:: python

    {% load wagtail_srcset_tags %}
    {% srcset_image img width-60 as thumbnail %}
    <a href="{{ thumbnail.original }}">
      <img id="img-{{ img.pk }}" src="{{ thumbnail.url }}" srcset="{{ thumbnail.srcset }}" />
    </a>

Features
--------

* Generate srcset attribute dynamically, based on the size of an image and
  the width attribute of the template tag if SRCSET_DYNAMIC is True
* You can specify default images sizes in DEFAULT_SRCSET_RENDITIONS
* wagtails WAGTAILIMAGES_JPEG_QUALITY is used for jpeg quality when set

Todo
----

* Dont just support the width resize-rule add fill, max, min etc

Documentation
-------------

The full documentation is at https://wagtail-srcset.readthedocs.io.

What is this all about?
-----------------------
I tried to use wagtail as a basis for a personal blog engine (yeah I know).
Playing around with some images I noticed that they looked not as sharp as
on my old page and I wondered why. Finally I found out that wagtail images
with width-600 for example are implicitly upscaled on modern display devices.
For a more detailed description and demonstration with an actual image,
take a look at the image below and maybe view it at 100% scale.

.. _wagtail: https://https://wagtail.io/
.. image:: https://github.com/ephes/wagtail_srcset/raw/main/example/media/wagtail_srcset.jpg

Here are two amplified sections, to make the difference more visible:

.. image:: https://github.com/ephes/wagtail_srcset/raw/main/example/media/ape_blurry.jpg
.. image:: https://github.com/ephes/wagtail_srcset/raw/main/example/media/ape_sharp.jpg

This package aims to provide a new image tag for wagtail that produces sharp
looking images by generating a srcset attribute that includes larger images
for higher pixel density devices.

If you are concerned about the increased image size I would recommend to use
more aggressive lossy compression instead of upscaling.



Running Tests
-------------

Does the code actually work?

::

    # create a virtualenv and activate it
    git clone https://github.com/ephes/wagtail_srcset.git
    cd wagtail_srcset
    python -m pip install flit
    flit install -s
    pytest

Running the Example App
-----------------------


::

    # activate virtualenv where wagtail_srcset is installed
    python manage.py runserver --settings example.settings 0.0:8000

Run Linter
----------

::

    # activate virtualenv where wagtail_srcset is installed
    flake8 wagtail_srcset tests

Coverage
--------

::

    # activate virtualenv where wagtail_srcset is installed
    pytest --cov=wagtail_srcset --cov-report=html

Start a Notebook Server
-----------------------

::

        # activate virtualenv where wagtail_srcset is installed
        DJANGO_ALLOW_ASYNC_UNSAFE=true python manage.py shell_plus --notebook


Build Documentation
-------------------

::

        # activate virtualenv where wagtail_srcset is installed
        rm docs/modules.rst docs/wagtail_srcset.rst
        sphinx-apidoc -o docs/ wagtail_srcset
        make -C docs clean
        make -C docs html
        open docs/_build/html/index.html


Publish Package
---------------

::

    # activate virtualenv where wagtail_srcset is installed
    flit publish
