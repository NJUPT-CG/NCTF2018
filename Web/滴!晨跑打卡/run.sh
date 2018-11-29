#!/bin/bash

service apache2 start

while test "1" = "1"
do
sleep 1000
done

/usr/bin/tail -f /dev/null

