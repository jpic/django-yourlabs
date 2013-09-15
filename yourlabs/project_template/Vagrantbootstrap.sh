#!/usr/bin/env bash
apt-get update
apt-get install -y nginx
/etc/init.d/nginx start

mkdir -p /srv/{{ project_name }}/
ln -sfn /vagrant /srv/{{ project_name }}/{{ project_name }}
