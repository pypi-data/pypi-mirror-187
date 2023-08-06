# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atcoder_auto_test']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-vision', 'numpy>=1.24.1,<2.0.0', 'online-judge-tools', 'pillow']

entry_points = \
{'console_scripts': ['s = atcoder_auto_test.main:submit',
                     't = atcoder_auto_test.main:test']}

setup_kwargs = {
    'name': 'atcoder-auto-test',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Kaji Keisuke',
    'author_email': 'kei.kyazikyazi@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
