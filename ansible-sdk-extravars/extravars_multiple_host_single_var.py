import asyncio


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    job_options = {
        'playbook': 'extravars_multiple_host_single_var.yml',
        'extra_vars': {
            'extra_variable': '1',
        },
    }
    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
