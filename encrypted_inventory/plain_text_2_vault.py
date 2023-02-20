from ansible.parsing.dataloader import DataLoader
from ansible.parsing import vault
from ansible.parsing.vault import VaultSecret
from ansible.module_utils._text import to_bytes, to_text, to_native
import sys

password = sys.argv[1]
secret_text = sys.argv[2]

new_loader = DataLoader()
secret = VaultSecret(to_bytes(password))
secret_obj = [('default', secret)]
bobs_vault = vault.VaultLib(secret_obj)
ciphertext = bobs_vault.encrypt(secret_text, vault.match_encrypt_secret(secret_obj)[1])
print(str(ciphertext.rstrip()))