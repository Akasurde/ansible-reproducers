import asyncio
import os


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    with open(os.path.join(os.getcwd(), 'datadir', 'env', 'cmdline'), 'w') as f:
        f.write("--vault-password-file=./get_password.sh")

    job_options = {
        'datadir': os.path.join(os.getcwd(), "datadir"),
        'role': 'enc_role',
        'roles_path': os.getcwd() + "/roles",
    }
    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
