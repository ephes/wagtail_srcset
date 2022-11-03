=====
Usage
=====

To use wagtail-srcset in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "wagtail_srcset.apps.WagtailSrcsetConfig",
        ...
    )

Add wagtail-srcset's URL patterns:

.. code-block:: python

    from wagtail_srcset import urls as wagtail_srcset_urls


    urlpatterns = [
        ...
        path("", include(wagtail_srcset_urls)),
        ...
    ]
