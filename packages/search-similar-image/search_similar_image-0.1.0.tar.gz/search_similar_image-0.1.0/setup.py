# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['search_similar_image',
 'search_similar_image.model',
 'search_similar_image.utils']

package_data = \
{'': ['*']}

install_requires = \
['faiss-cpu>=1.7.3,<2.0.0', 'pdoc3>=0.10.0,<0.11.0', 'timm>=0.6.12,<0.7.0']

setup_kwargs = {
    'name': 'search-similar-image',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'tocom',
    'author_email': 'tcom242242@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tocom242242',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
