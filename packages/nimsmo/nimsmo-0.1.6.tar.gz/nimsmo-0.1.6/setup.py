# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nimsmo']

package_data = \
{'': ['*'], 'nimsmo': ['kernel/*', 'problem/*']}

install_requires = \
['nython>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'nimsmo',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Installation\n\n## Installation of nim package\n\n```\nnimble install\n```\n\nRun example:\n\n```\nnim r -d:release examples/smo_test.nim\n```\n\n## Installation of python module\n\n### from PyPi\n```\npip install nimsmo\n```\n\n### from source\nFirst, install dependencies:\n```\nconda install poetry\n```\n\n\n```\npoetry shell\npoetry install\n```\n\nRun example:\n\n```\npython examples/smo_test.py\n```\n',
    'author': 'Nico Strasdat',
    'author_email': 'Nico.Strasdat@tu-dresden.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build_nim import *
build(setup_kwargs)

setup(**setup_kwargs)
