#!/bin/bash

export VAULT_ADDR='http://127.0.0.1:8200'
vault login -method=userpass username=ansible_user password=${ansible_user_vault_login_password} > /dev/null 2>&1
vault kv get -mount=secret -field=value testproject/vault_passwd
