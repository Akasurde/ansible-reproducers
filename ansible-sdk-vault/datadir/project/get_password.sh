#!/bin/bash
# Export these
# export VAULT_ADDR='http://127.0.0.1:8200'
# export VAULT_TOKEN=""

vault kv get -field=ansible_vault_secret secret/ansiblepwd
