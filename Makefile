.POSIX:

env ?= staging
vault_id ?= alpina@contrib/rbw-client.sh

all: site

setup:
	poetry install --quiet

site: setup
	poetry run ansible-playbook --vault-id ${vault_id} -i inventories/${env} site.yml

services: setup
	poetry run ansible-playbook --vault-id ${vault_id} -i inventories/${env} services.yml
