.POSIX:
.PHONY: *
.EXPORT_ALL_VARIABLES:
MAKEFLAGS += -r # no use of built-in rules

env ?= staging
vault_id ?= alpina@contrib/rbw-client.sh

playbook_cmd := poetry run ansible-playbook --vault-id ${vault_id} -i inventories/${env}

all: site services

setup:
	poetry install --quiet

site: setup
	 $(playbook_cmd) site.yml

services: setup
	$(playbook_cmd) services.yml

clean: setup
	$(playbook_cmd) clean.yml
