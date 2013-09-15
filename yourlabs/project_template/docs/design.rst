Basic rules
-----------

- source code should be editable by line
- indentation is 4 spaces
- every child line of code must have one indentation level from its
  parent
- I will revert commits which contain poorly formated code !



Example of how the HTML should be indented::

    {% verbatim %}
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
    {% endverbatim %}

..
   Local Variables:
   mode: rst
   fill-column: 79
   End:
   vim: et syn=rst tw=79
