# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['statgis', 'statgis.gee', 'statgis.statutils']

package_data = \
{'': ['*']}

install_requires = \
['earthengine-api>=0.1.335',
 'matplotlib>=3.2.2',
 'pandas>=1.3.5',
 'scipy>=1.7.3']

setup_kwargs = {
    'name': 'statgis',
    'version': '1.0.4',
    'description': 'Tools for improve work with geospatial data in Python',
    'long_description': '# StatGIS Python Package\n\n![PyPI](https://img.shields.io/pypi/v/statgis) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/statgis?color=yellow) [![Documentation Status](https://readthedocs.org/projects/statgis/badge/?version=latest)](https://statgis.readthedocs.io/en/latest/?badge=latest)\n\nStatGIS help to the users to process and analyse satellite images in Google Earth Engine.\n\n## Installation\n\n```bash\n$ pip install statgis\n```\n\n## Usage\n\nIn this package you could find function to scale optical images, classify images,\ncharacterize shorelines and much more.\n\n```python\n# Example: mask clouds and scale to reflectance values\nimport ee\nfrom statgis.gee import landsat_functions\n\nee.Initialize()\n\nimage_collection = (\n    ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")\n      .map(landsat_functions.cloud_mask)\n      .map(landsat_functions.scaler)\n)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`statgis` was created by Sebástian Narváez-Salcedo, Brayan Navarro-Londoño. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`statgis` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Sebástian Narváez-Salcedo',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
