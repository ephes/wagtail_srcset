=============================
wagtail-srcset
=============================

.. image:: https://badge.fury.io/py/wagtail-srcset.svg
    :target: https://badge.fury.io/py/wagtail-srcset

.. image:: https://travis-ci.org/ephes/wagtail_srcset.svg?branch=master
    :target: https://travis-ci.org/ephes/wagtail_srcset

.. image:: https://codecov.io/gh/ephes/wagtail_srcset/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ephes/wagtail_srcset

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ephes/wagtail-srcset

HTML5 image srcset support for Wagtail

What is this all about?
-----------------------
I tried to use wagtail as a basis for a personal blog engine (yeah I know).
Playing around with some images I noticed that they looked not as sharp as
on my old page and I wondered why. Finally I found out that wagtail images
with width-600 for example are implicitly upscaled on modern display devices.
For a more detailed description and demonstration with an actual image,
take a look at the image below and maybe view it at 100% scale.

.. _wagtail: https://https://wagtail.io/
.. image:: https://github.com/ephes/wagtail_srcset/raw/master/example/media/wagtail_srcset.jpg

Here are two amplified sections, to make the difference more visible:

.. image:: https://github.com/ephes/wagtail_srcset/raw/master/example/media/ape_blurry.jpg
.. image:: https://github.com/ephes/wagtail_srcset/raw/master/example/media/ape_sharp.jpg

This package aims to provide a new image tag for wagtail that produces sharp
looking images by generating a srcset attribute that includes larger images
for higher pixel density devices.

If you are concerned about the increased image size I would recommend to use
more aggressive lossy compression instead of upscaling.

Documentation
-------------

The full documentation is at https://wagtail-srcset.readthedocs.io.

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

Features
--------

* Generate srcset attribute dynamically, based on the size of an image and
  the width attribute of the template tag if SRCSET_DYNAMIC is True
* You can specify default images sizes in DEFAULT_SRCSET_RENDITIONS
* wagtails WAGTAILIMAGES_JPEG_QUALITY is used for jpeg quality when set

Todo
----

* Dont just support the width resize-rule add fill, max, min etc

Running Tests
-------------

Does the code actually work?

::

    git clone https://github.com/ephes/wagtail_srcset.git
    cd wagtail_srcset
    poetry install
    poetry run test

Running the Example App
-----------------------


::

    poetry shell
    python manage.py runserver --settings example.settings 0.0:8000

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
