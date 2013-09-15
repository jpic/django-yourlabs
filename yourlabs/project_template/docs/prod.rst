Deploying this project
======================

This chapter covers deployment of this project.

Static files update
-------------------

When adding a new file in `{{ project_name }}/static/`, you should
command django to update `{{ project_name }}/public/static/`
symlinks::

    ./manage.py collectstatic -l

Database setup
--------------

Database schema update
----------------------

Database migrations are handled by south, execute them with::

    ./manage.py migrate

In case new tables were created by apps which are not managed by
south, run::

    ./manage.py syncdb

Index update
------------

If anything changed in `templates/search/indexes/`, then it would
be a good idea to re-index all data::

    ./manage.py rebuild_index

Nginx configuration
-------------------

Add this server entry to `nginx.conf`::

    server {
        listen 80;
        server_name your_project.com localhost;

        # this may be in your http {} configuration instead
        include uwsgi_params;

        location /public/ {
            alias /srv/{{ project_name }}/public/;
        }
        
        location / {
            uwsgi_pass unix:/tmp/uwsgi_{{ project_name }}.sock;
        }   
    }

Run `nginx -s reload` to reload nginx.

uWSGI configuration
-------------------

Create a file called `{{ project_name }}.ini`. It is important
that it is called `{{ project_name }}.ini` because it contains
`%n` which is a magic variable and will be replaced with `{{
project_name }}` by uWSGI. This would be a good start::

    [uwsgi]
    plugin=python2

    env=DJANGO_SETTINGS_MODULE=%n.settings.prod
    chdir=/srv/%n
    venv=/srv/%n/env

    socket=/tmp/uwsgi_%n.sock
    pidfile=/tmp/uwsgi_%n.pid
    daemonize=/var/log/uwsgi/%n.log

    module=%n.wsgi:application

    close-on-exec = 1
    harakiri = 120
    max-requests = 00
    processes = 4
    master = 1  
    uid = 1004
    gid = 33
    chmod=666   
    log-5xx = 1 
    vacuum = 1
    post-buffering = 8192

Start uWSGI with an emperor on the parent directory or with `uwsgi
{{ project_name }}.ini`.

..
   Local Variables:
   mode: rst
   fill-column: 79
   End:
   vim: et syn=rst tw=79
