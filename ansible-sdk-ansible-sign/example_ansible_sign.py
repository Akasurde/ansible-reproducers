import asyncio
import os
from ansible_sign.cli import main as ansible_sign_main


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout

def check_integrity():
    project_dir = "%s/datadir" % os.getcwd()
    print("Checking integrity for %s" % project_dir)
    ret = ansible_sign_main(['project', 'gpg-verify', project_dir])
    return ret

async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    job_options = {
        'playbook': 'ansible_sign_demo.yml',
        'extra_vars': {
            'extra_variable': '1',
        },
    }
    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    ret = check_integrity()
    if ret == 0:
        asyncio.run(main())
