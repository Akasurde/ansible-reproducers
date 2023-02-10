base_dir=`pwd`

vault_bin=vault
nohup ${vault_bin} server -dev -config ${base_dir}/vault_config.hcl &
sleep 10
cat ${base_dir}/policy.hcl | ${vault_bin} policy write admins -
${vault_bin} kv put -mount=secret testproject/mysql_passwd value=Secret123
${vault_bin} kv put -mount=secret testproject/vault_passwd value=Secret123
${vault_bin} auth enable userpass
${vault_bin} write auth/userpass/users/ansible_user password=Secret123 policies=admins
