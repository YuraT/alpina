.POSIX:
.PHONY: *
.EXPORT_ALL_VARIABLES:

env ?= staging
vault_id ?= alpina@contrib/rbw-client.sh

clean_desired ?= false

all: site

setup:
	poetry install --quiet

site: setup
	poetry run ansible-playbook --vault-id ${vault_id} -i inventories/${env} --extra-vars "clean_desired_arg=${clean_desired}" site.yml

services: setup
	poetry run ansible-playbook --vault-id ${vault_id} -i inventories/${env} services.yml
