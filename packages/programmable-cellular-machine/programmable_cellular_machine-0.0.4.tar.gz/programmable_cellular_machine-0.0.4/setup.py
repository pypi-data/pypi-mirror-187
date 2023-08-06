# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['programmable_cellular_machine', 'programmable_cellular_machine.hight']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pillow>=9.3.0,<10.0.0',
 'pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'programmable-cellular-machine',
    'version': '0.0.4',
    'description': 'Клеточный автомат, в котором можно задавать правила',
    'long_description': '# Программируемый клеточный автомат\n\nКлеточный автомат, в котором можно задавать правила, которые будут применяться к области.\n\n## Профилирование\n\n```bash\n# скорость\npoetry run python -m cProfile -o profile.prof main.py\npoetry run gprof2dot -f pstats profile.prof | dot -Tpng -o profile.png\n\n# память\npoetry run python -m memory_profiler main.py \n```\n\n## Contribute\n\nIssue Tracker: <https://gitlab.com/rocshers/python/programmable-cellular-machine/-/issues>  \nSource Code: <https://gitlab.com/rocshers/python/programmable-cellular-machine>\n',
    'author': 'irocshers',
    'author_email': 'develop.iam@rocshers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/rocshers/python/programmable-cellular-machine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
