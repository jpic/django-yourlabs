Developing this project
=======================

Basic rules
-----------

- source code should be editable by line
- source code should be `PEP8
  <http://www.python.org/dev/peps/pep-0008/>`_-compliant,
- if necessary, it should contain `PEP257
  <http://www.python.org/dev/peps/pep-0257/>`_ compliant
  docstrings,
- indentation is 4 spaces
- I will revert commits which contain poorly formated code !

Changing a model structure and database migrations
--------------------------------------------------

After adding, changing, removing a field or model from
`models.py`, generate a migration with such a command::

    ./manage.py schemamigration --auto <app_name>

Replace `<app_name>` with the name of your app. Then, apply the
migration with::

    ./manage.py migrate

Using the shell
---------------

A couple of shells are provided, `./manage.py shell` will run a Python shell,
and `./manage.py dbshell` will run a database shell.

For example, I could create an object from the Python shell and get it's
primary key like this::

    >>> ./manage.py shell
    Python 2.7.4 (default, Apr 19 2013, 18:35:44) 
    Type "copyright", "credits" or "license" for more information.

    IPython 0.13.2 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    In [1]: from cities_light.models import Country

    In [2]: new=Country(name='Test', continent='EU')

    In [3]: new.save()

    In [4]: print new.pk
    4

Using breakpoints to debug
--------------------------

To add a breakpoint in the code, add this code::

    import ipdb; ipdb.set_trace()

For example, if I place it in such a function::

    a=32

    def add(var, add):
        return var + add

    import ipdb; ipdb.set_trace()
    a=add(a, 1)
    a=add(a, 3)

Then, it would break like this::

    > /home/jpic/env/src/cities-light/test_project/test.py(7)<module>()
        6 import ipdb; ipdb.set_trace()
    ----> 7 a=add(a, 1)
        8 a=add(a, 3)

    ipdb> 

I could do a print statement to inspect a variable::

    ipdb> print a
    32
    ipdb> 

To continue the execution up to the next like, type `n`::

    ipdb> n
 
And it would break on next line::

    > /home/jpic/env/src/cities-light/test_project/test.py(8)<module>()
        7 a=add(a, 1)
    ----> 8 a=add(a, 3)
        9 a=add(a, 4)

    ipdb> 

I could inspect the variable again::
    
    ipdb> print a
    33
    ipdb> 
    
Or step into the function call::

    ipdb> s
    --Call--
    > /home/jpic/env/src/cities-light/test_project/test.py(3)add()
        2 
    ----> 3 def add(var, add):
        4     return var + add

    ipdb> 
    
Here, you can see that the cursor is on the function. Type `n` to move
forward::
    
    ipdb> n
    > /home/jpic/env/src/cities-light/test_project/test.py(4)add()
        3 def add(var, add):
    ----> 4     return var + add
        5 

Here, I could inspect variables. Type `c` to continue the execution of the
script until next breakpoint or until the end of the script.

You should now be able to debug any Python code.

..
   Local Variables:
   mode: rst
   fill-column: 79
   End:
   vim: et syn=rst tw=79
