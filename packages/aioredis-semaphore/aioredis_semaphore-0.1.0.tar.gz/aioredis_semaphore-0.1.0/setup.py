# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioredis_semaphore']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'aioredis-semaphore',
    'version': '0.1.0',
    'description': '',
    'long_description': '===============\naioredis-semaphore\n===============\n\n\nA distributed semaphore and mutex built on Redis.\n\n\nInstallation\n------------\nTo install aioredis-semaphore, simply::\n\n    pip install aioredis-semaphore\n\n\nExamples\n--------\n\n::\n\n    # -*- coding:utf-8 -*-\n    import anyio\n    from aioredis import Redis\n    from anyio import create_task_group, run\n\n    from aioredis_semaphore import Semaphore\n\n    semaphore = Semaphore(Redis(), count=2, namespace="example")\n\n\n    async def task(i: int) -> None:\n        async with semaphore:\n            print("id: {}".format(i))\n            print("sleep...")\n            await anyio.sleep(2)\n\n\n    async def main() -> None:\n        async with create_task_group() as tg:\n            for i in range(5):\n                tg.start_soon(task, i)\n\n\n    if __name__ == "__main__":\n        run(main)\n',
    'author': 'David Jiménez',
    'author_email': 'davigetto@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
