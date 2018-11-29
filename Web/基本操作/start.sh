#!/bin/bash

service apache2 start

service mysql start

tail -F /etc/passwd
