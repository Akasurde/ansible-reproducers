import asyncio
import os


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    datadir = os.path.join(os.getcwd(), "datadir")
    env_dir = os.path.join(datadir, 'env')
    roles_path = os.path.join(os.getcwd(), "roles")

    if not os.path.exists(env_dir):
        os.mkdirs(env_dir)

    with open(os.path.join(env_dir, 'cmdline'), 'w') as f:
        f.write("--vault-password-file=./get_password.sh")

    job_options = {
        'datadir': datadir,
        'role': 'enc_role',
        'roles_path': roles_path,
    }
    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
