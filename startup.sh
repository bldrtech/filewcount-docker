#!/bin/sh
service nginx start
uwsgi --ini /etc/uwsgi/apps-enabled/upload.ini