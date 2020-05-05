#!/bin/sh

while [ -z $(netstat -lnt | awk '$4 ~ /:8080$/') ]; do
  echo "Waiting for tap to launch on 8080..."
  sleep 1 # wait for 1/10 of the second before check again
done

sleep 3
nc -d localhost 8080 | target-postgres -c /etc/config/target.json >> /etc/config/state.json
write_state -c /etc/config/target.json

echo "Done"
