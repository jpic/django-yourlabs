{% verbatim %}
Basic rules
-----------

- source code should be editable by line
- indentation is 4 spaces
- every child line of code must have one indentation level from its
  parent
- I will revert commits which contain poorly formated code !

HTML coding style example
-------------------------

Example of how the HTML should be indented::

    {% block bar %}
    <div>
        {% if foo %}
        <div class="{% if foo.active %}active{% endif %}">
            <p>
            It doesn't matter if contents is indented
            </p>
        </div>
        {% endif %}
    <div>
    {% endblock %}

Template location
-----------------

What template is being used ?
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

To find out what template is used in a page, click on the `DjDt`
image on the right of the page. It will reveal the Django Debug
Toolbar.

In the toolbar, there is a Templates tab which lists all templates
used to generate the page.

Template overriding
>>>>>>>>>>>>>>>>>>>

If a template is located outside the project directory, then this
means that you should not edit it. To edit a template from outside
the project directory, override the template first.

To override a template, simply copy it from its original location
into the `templates/` sub-directory of the project.

For example, if my project is in `/home/jpic/my_project` and I want
to modify
`/home/jpic/env/lib/python/site-packages/django/contrib/admin/base.html`,
then I would copy it in
`/home/jpic/my_project/templates/admin/base.html`.

I can safely edit `templates/admin/base.html`.

Variables in templates
----------------------

To display a variable in a template, use `{{` and `}}`. For example, if
`your_variable` is `world` then::

    Hello {{ your_variable }}

Will render as::

    Hello world

Template tags and filters
-------------------------

A template filter changes a variable. For example, the `capfirst` template
filter capitalizes the first letter of a variable::

    Hello {{ your_variable|capfirst }}

Will render as:

    Hello World

A template tag is like a new function in the template language. It make take
variables as arguments as is called with `{%` and `%}` like this::

    {% thumbnail your_image 200x200 %}

Some template tags require closing tags, for example to show some contents only
in `your_variable` is set::

    {% if your_variable %}
        Hello {{ your_variable }}
    {% endif %}

Make sure that you consult:

- `The Django template language documentation
  <https://docs.djangoproject.com/en/dev/topics/templates/>`_,
- `Built-in template tags and filters list on Django documentation
  <https://docs.djangoproject.com/en/dev/ref/templates/builtins/>`_,
- In your development domain, use `/admin/doc/tags/` to find the list of all
  installed template tags and filters. For example:
  `http://localhost:8000/admin/doc/tags/`.

Custom template tags
--------------------

Static files
------------

Where are static files ?
>>>>>>>>>>>>>>>>>>>>>>>>

Static files are files like 'jquery.js' or 'style.css' or
'menu.jpg'. Those should live in the `static/` subdirectory of the
project.

Never hardcode a url
>>>>>>>>>>>>>>>>>>>>

You should never hardcode a url like this::

    <script src="/static/jquery.js" type="text/javascript"></script>

.. danger::
   In Django, we **never** hardcode any URL !

`{% static %}` template tag usage
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Instead, you should generate the url with the `{% static %}`
template tag. To enable the `{% static %}` template tag, add in
your template::

    {% load static %}

Now, you can generate a static file url properly as such::

    <script src="{% static 'jquery.js' %}" type="text/javascript"></script>

The advantage of this technique is that we can decide to host our
static files on a CDN later on without changing our code.

Paths
>>>>>

Paths for `{% static %}` are relative to `static/`.

If your static file is in `static/js/foo.js`, then your template tag should
look like `{% static 'js/foo.js' %}`.

Template inheritance
--------------------

Template inheritance is the opposite of `include()`. For example, if I have two
pages on urls `/home/` and `/contact/`, then I could have three templates like this:

- `base.html`::

  <html>
      <head>
          <!-- blabla -->
      </head>
      <body>
          <div class="container">
          {% block body %}
          {% endblock %}
      </body>
  </html>

- `home.html`::

  {% extends 'base.html' %}

  {% block body %}
  Welcome on our homepage !
  {% endblock %}

- `contact.html`::

  {% extends 'base.html' %}

  {% block body %}
  Contact us at: 0123467856
  {% endblock %}

What happens is that a `{% block block_name %}{% endblock %}` of `base.html` is
overridden in `home.html` or `contact.html` just like a CSS property.

Internationalization
--------------------

`{% trans %} template tag`
>>>>>>>>>>>>>>>>>>>>>>>>>>

Our project should support several languages. So we can't hard-code any text
like this::

    Hello world

Because that text will always be rendered as `Hello world`. If we want this
text to be rendered as `Bonjour monde` in French, then we should use the `{%
trans %}` template tag as such::

    {% load i18n %}

    {% trans 'Hello world' %}

Now, assuming that someone has added the translation for `Hello world`, this
could potentially render in any language.

Note that we have loaded the `{% trans %}` template tag with `{% load i18n %}`.

`{% blocktrans %} template tag`
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

In our project, we will never hardcode text, instead, we will always use `{%
trans %}` or `{% blocktrans %}`. 

You need `{% blocktrans %}` if you need a variable in your text. This is how
`{% blocktrans %}` works::

    {% blocktrans %}Hello {{ your_variable }}{% endblocktrans %}

This is because, in English you would say `The red car` but in french you would
say `La voiture rouge`. So, this in the template::

    {% blocktrans %}The {{ color }} {{ object }}{% endblocktrans %}

Would create a translation string of `The {{ color }} {{ object }}`. In the
french translation file, this would be translated by `La {{ object }} {{ color
}}` which has an inversion of variable position.

URLs
----

Never hardcode a url
>>>>>>>>>>>>>>>>>>>>

You should never hardcode a url like this::

    <a href="/home/">{% trans 'Home' %}</a>

.. danger::
   In Django, we **never** hardcode any URL !

Because, maybe the url should be `/accueuil/` in French, or maybe
it will change to `/your-home/`.

`{% url %}` template tag
>>>>>>>>>>>>>>>>>>>>>>>>

In Django, we generate urls. You can generate urls with the `{% url
%}` template tag::

    <a href="{% url 'home' %}">{% trans 'Home' %}</a>

LessCSS
-------

In `static/main.less`, you can use `LessCSS <http://lesscss.org>`_ instead of
plain old, boring CSS. You can also re-use functions defined by
`bootstrap.less` too.

{% endverbatim %}

..
   Local Variables:
   mode: rst
   fill-column: 79
   End:
   vim: et syn=rst tw=79
