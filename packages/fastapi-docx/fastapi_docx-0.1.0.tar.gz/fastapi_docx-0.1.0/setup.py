# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_docx']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0']

setup_kwargs = {
    'name': 'fastapi-docx',
    'version': '0.1.0',
    'description': 'Extend a FastAPI OpenAPI spec to include all possible HTTPException or custom Exception response schemas.',
    'long_description': '# fastapi-docx\nExtend a FastAPI OpenAPI spec to include all possible HTTPException or custom Exception response schemas.\n',
    'author': 'Saran Connolly',
    'author_email': 'saran@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Saran33/fastapi-docx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.1,<4.0.0',
}


setup(**setup_kwargs)
