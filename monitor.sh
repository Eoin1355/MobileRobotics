#!/bin/bash
sleep 60
if ! curl -f -m 10 http://3.250.38.184:8000/; then
    supervisorctl restart guni:*
    exit 1
else
    supervisorctl restart check_django_endpoint:*
fi