#!/usr/bin/env bash
echo export LANGUAGE=en_US.UTF-8 > /etc/bash.bashrc
echo export LANG=en_US.UTF-8 > /etc/bash.bashrc
echo LC_ALL=en_US.UTF-8 > /etc/bash.bashrc
locale-gen en_US.UTF-8
dpkg-reconfigure locales

apt-get update
apt-get install -y nginx uwsgi-plugin-python postgresql-9.1 python-virtualenv memcached python-imaging python-psycopg2 python-pylibmc nodejs npm git 
npm install -g coffee-script recess


su postgres -c 'psql -f /vagrant/docs/examples/postgresql_utf8_template.sql'
su postgres -c 'createuser -wsrd vagrant'
su postgres -c 'createdb -E UTF8 -O vagrant django'

mkdir -p /srv/{{ project_name }}/
ln -sfn /vagrant /srv/{{ project_name }}/{{ project_name }}

virtualenv --system-site-packages /srv/{{ project_name }}/env
source /srv/{{ project_name }}/env/bin/activate
pip install -r /srv/{{ project_name }}/{{ project_name }}/requirements/base.txt
pip install django

ln -sfn /vagrant/docs/examples/nginx.conf /etc/nginx/nginx.conf

/etc/init.d/nginx start
echo DJANGO_SETTINGS_MODULE={{ project_name }}.settings.vagrant >> /etc/bash.bashrc
export DJANGO_SETTINGS_MODULE={{ project_name }}.settings.vagrant
/srv/{{ project_name }}/{{ project_name }}/manage.py syncdb --noinput
/srv/{{ project_name }}/{{ project_name }}/manage.py migrate
chown -R vagrant /srv/{{ project_name }}/env
chown vagrant /srv/{{ project_name }}

uwsgi --ini /vagrant/docs/examples/{{ project_name }}.ini

echo Please enter password for superuser 'test'
/srv/{{ project_name }}/{{ project_name }}/manage.py createsuperuser
