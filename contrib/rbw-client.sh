#!/usr/bin/env bash

# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash

while [[ $# -gt 0 ]]; do
  case $1 in
    --vault-id)
      vault_id="$2"
      shift # past argument
      shift # past value
      ;;
    -*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

# rbw adds a newline which has to be trimmed
/usr/bin/env rbw get --folder Keyring "$vault_id" ansible_vault | tr -d '\n'
