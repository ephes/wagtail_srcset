=============================
wagtail-srcset
=============================

.. image:: https://badge.fury.io/py/wagtail-srcset.svg
    :target: https://badge.fury.io/py/wagtail-srcset

.. image:: https://travis-ci.org/spielmann/wagtail-srcset.svg?branch=master
    :target: https://travis-ci.org/spielmann/wagtail-srcset

.. image:: https://codecov.io/gh/spielmann/wagtail-srcset/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/spielmann/wagtail-srcset

HTML5 image srcset support for Wagtail

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
        'wagtail_srcset.apps.WagtailSrcsetConfig',
        ...
    )

Add wagtail-srcset's URL patterns:

.. code-block:: python

    from wagtail_srcset import urls as wagtail_srcset_urls


    urlpatterns = [
        ...
        url(r'^', include(wagtail_srcset_urls)),
        ...
    ]

Image
-----
.. image:: https://github.com/ephes/wagtail_srcset/raw/master/example/media/wagtail_srcset.jpg

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
