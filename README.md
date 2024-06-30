# Alpina

A home for configuring all of my homelab containers on a Debian Linux machine.
This assumes a Debian Linux machine with Docker and Docker Compose installed.

My particular setup is based on a [jailmaker](https://github.com/Jip-Hop/jailmaker) container
running on top of TrueNAS SCALE, separating all the docker stuff from the appliance.

# Notes

## IPv6
The current configuration is designed to work with IPv6. 
However, because of how (not properly) I'm doing the subnetting 
from the host's network, NDP doesn't work.
This means that container IPs are not accessible from other hosts on the local network.
I simply have a static route on my router to the container subnet, 
that uses the IP of this host as the gateway.

This is a limitation of my current ISP, I only have a single /64 subnet for my lab network.
I'd like to get a /56 or /48, perhaps using Hurricane Electric's tunnel broker.
*Sigh* ISPs being stingy with the 2^48 prefixes they're afraid of running out of.

## Upgrading Postgres
Upgrading the postgres container for a given stack requires a dump and restore.

After making a snapshot or backup of postgres data directory,
in the compose directory for a given stack, run the following commands:
```bash
docker compose down
docker compose up -d <db_service>
docker compose exec -it <db_service> pg_dumpall -U <db_user> | tee /tmp/dump.sql
docker compose down

rm -r <postgres_data_dir>/*  # as root
# Edit the docker-compose.yml file to use the new postgres image
docker compose up -d <db_service>
# For some reason, compose exec doesn't like the input redirection
docker exec -i <db_container_name> psql -U <db_user> < /tmp/dump.sql
docker compose up -d
rm /tmp/dump.sql
```

Additionally, if upgrading from postgres <= 13, it is necessary to upgrade the
password hashes. This can be done by running the following command:
```bash
docker compose exec -it <db_service> psql -U <db_user> -c "\password"
```
