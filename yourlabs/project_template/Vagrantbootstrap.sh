#!/usr/bin/env bash
#echo export LANGUAGE=en_US.UTF-8 > /etc/bash.bashrc
#echo export LANG=en_US.UTF-8 > /etc/bash.bashrc
#echo LC_ALL=en_US.UTF-8 > /etc/bash.bashrc
#locale-gen en_US.UTF-8
#dpkg-reconfigure locales

apt-get update

touch /tmp/installscript
chmod +x /tmp/installscript

function install_db {
    sudo apt-get install -y postgresql-9.1

    cat > /tmp/installscript <<EOF
#!/usr/bin/env bash
psql -f /vagrant/docs/examples/postgresql_utf8_template.sql
createuser -wsrd vagrant
createdb -E UTF8 -O vagrant django
EOF
    su postgres -c /tmp/installscript
        
    cat > /tmp/installscript <<EOF
export DJANGO_SETTINGS_MODULE={{ project_name }}.settings.vagrant
source /srv/{{ project_name }}/env/bin/activate
cd /srv/{{ project_name }}
./manage.py syncdb --noinput
./manage.py migrate
EOF
    su vagrant -c /tmp/installscript
}

function install_http {
    apt-get install -y nginx uwsgi-plugin-python nodejs npm memcached
    npm install -g coffee-script recess

    ln -sfn /vagrant/docs/examples/nginx.conf /etc/nginx/nginx.conf
    /etc/init.d/nginx start
    uwsgi --ini /vagrant/docs/examples/{{ project_name }}.ini
}

function install_project {
    echo DJANGO_SETTINGS_MODULE={{ project_name }}.settings.vagrant >> /etc/bash.bashrc
    
    apt-get install -y git python-virtualenv python-imaging python-psycopg2 python-pylibmc

    ln -sfn /vagrant /srv/{{ project_name }}
    chown vagrant /srv/{{ project_name }}

    cat > /tmp/installscript <<EOF
#!/usr/bin/env bash
virtualenv --system-site-packages /srv/{{ project_name }}/env
source /srv/{{ project_name }}/env/bin/activate
pip install django
pip install -r /srv/{{ project_name }}/requirements/base.txt
EOF
    su vagrant -c /tmp/installscript
}

install_project
install_db

