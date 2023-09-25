import asyncio
from cryptography.fernet import Fernet
import os
import tempfile
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout, run_one_events, run_many


async def main():
    # Datadir to store the playbook
    datadir = os.path.join(os.getcwd(), 'datadir')
    # Secret Key to encrypt the ansible-vault password
    secret_key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
    
    fernet = Fernet(secret_key.encode())
    # Ansible vault password
    ansible_vault = 'Secret123'
    # Encrypt the ansible vault password and store in the database
    enc_ansible_vault = fernet.encrypt(ansible_vault.encode())

    # Retrieve the encrypted ansible vault password
    # Decrypt the encrypted ansible vault password
    decrypt_ansible_vault = fernet.decrypt(enc_ansible_vault).decode()
    # Create a temp file to store the ansible vault password
    tf = tempfile.NamedTemporaryFile(delete=False)
    with open(tf.name, "w") as f:
        f.write(decrypt_ansible_vault)

    # Use the password filename as ansible-sdk API using 'env/cmdline'
    with open(os.path.join(datadir, 'env', 'cmdline'), 'w') as f:
        f.write(f"--vault-password-file={tf.name}")

    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()
    # Use vault encrypted playbook
    job_options = {
        'datadir': datadir,
        'playbook': 'vault.yml'
    }

    ret = await run_one_stdout(executor, executor_options, job_options=job_options)
    tf.close()
    os.unlink(tf.name)

if __name__ == '__main__':
    asyncio.run(main())
