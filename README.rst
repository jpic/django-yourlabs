django-yourlabs
~~~~~~~~~~~~~~~

.. image:: https://travis-ci.org/jpic/django-yourlabs.png?branch=master   
   :target: https://travis-ci.org/jpic/django-yourlabs

django-yourlabs has a starter project and a few commands. It can run either on
any OS with vagrant with `startproject --vagrant` or on the local venv of your
linux box with `startproject --local`.

Get started right away on your linux box:

    virtualenv your_project_env
    source your_project_env/bin/activate
    pip install -e git+https://github.com/jpic/django-yourlabs.git#egg=yourlabs
    yl startproject --local your_project
    # vagrant up if you want to run it on viagrant with postgresql etc ...

Or on Windows, Mac:

    pip install -e git+https://github.com/jpic/django-yourlabs.git#egg=yourlabs
    yl startproject --vagrant your_project
    # open http://localhost:10080
    # vagrant ssh and visit /vagrant for logs and the project.

Project template
================

The project template has:

- lessCSS & bootstrap, allows to code in lessCSS using bootstrap API in less
- jQuery, coffeescript,
- relevant settings which work out of the box, organnised in accordance with
  best practices
- internationalization out of the box,
- Vagrant,
- my favorite apps out of the box:

  - django-responsive-admin,
  - sphinx for project and app documentation,
  - django-debug-toolbar with plugins,
  - django-extensions,
  - ipdb,
  - django-easy-thumbnails,
  - django-haystack with whoosh,
  - django-reversion,
  - django-modeltranslation,
  - south,
  - django-compressor (support for less and coffee),
  - django-autocomplete-light,

`yourlabs` package
==================

As a python package, it provides a command `yl`  which barely decorates
`django-admin.py`, giving priority to django-yourlab's commands. To use the
normal Django commands, just use `django-admin.py` or `manage.py`.

Currently, `yl` only provides the decorated `startproject` command, see `yl
startproject --help` for more info.

As an app, it provides:

`yourlabs.context_processors.expose_settings` 
    A simple context processor handling `{{ settings }}` based on
    `settings.EXPOSE_SETTINGS`. For example if
    `EXPOSE_SETTINGS=['COMPRESS_ENABLED']` then `{{ settings.COMPRESS_ENABLED }}`
    becomes available in the context.
    As simple as it sounds, it server a greater purpose: it allows less css to
    be compiled client side by `less.js` which provides better debugging info
    than the server side compiler. This is particularely useful when the CSS
    programer is unable to see the development server console.

It also provides the following commands for fun:

- `yl_commands <app> <command-name>` will create
  `app/management/commands/<command-name>.py`,
- `yl_urls <app>` adds `app/urls.py`,

Note: you can easely override templates even at project level, and create new
commands using templates to generate basic code.

TODO
====

- `yl_views <app>` parses `app/urls.py` and creates `app/views.py`,
- `yl_templates <app>` adds `app/templates/app/base.html`, which all templates
  in `app/templates/app/` should extend (best practice). Also, it parses
  `app/urls.py` and `app/views.py` to find template names to create if
  necessary.
- `yl_locale <app> <language-code>` will prepare/update
  `app/locale/<language-code>/LC_MESSAGES/django.po` for translation.
- `yl_haystack <app>` will parse `app/models.py` and create
  `app/search_indexes.py`,
- `yl_autocomplete_light <app>` will parse `app/models.py` and create
  `app/autocomplete_light_registry.py`,
