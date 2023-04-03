# Alpina

A home for configuring all of my homelab containers on a Debian Linux machine.
This assumes a Debian Linux machine with Docker and Docker Compose installed.

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
