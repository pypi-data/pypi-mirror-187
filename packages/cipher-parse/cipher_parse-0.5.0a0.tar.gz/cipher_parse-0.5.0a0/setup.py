# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipher_parse',
 'cipher_parse.example_data',
 'cipher_parse.example_data.dream3d.2D',
 'cipher_parse.example_data.dream3d.3D']

package_data = \
{'': ['*']}

install_requires = \
['damask>=3.0.0-alpha.6,<4.0.0',
 'h5py==2.10.0',
 'ipywidgets<8.0.0',
 'itkwidgets>=0.25.2',
 'nbformat>=5.4.0,<6.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'parse>=1.19.0,<2.0.0',
 'plotly>=5.9.0,<6.0.0',
 'pyvista>=0.34.2,<0.35.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'vecmaths>=0.1.6,<0.2.0']

extras_require = \
{'hickle': ['hickle==4.0.4'],
 'matflow': ['hickle==4.0.4', 'matflow>=0.2.26,<0.3.0'],
 'notebook': ['notebook>=6.5.1,<7.0.0']}

setup_kwargs = {
    'name': 'cipher-parse',
    'version': '0.5.0a0',
    'description': 'Pre- and post-processing for the phase-field code CIPHER.',
    'long_description': '# cipher-parse\n\n**Pre- and post-processing for the phase-field code [CIPHER](https://github.com/micmog/CIPHER)**\n\n[![PyPI version](https://img.shields.io/pypi/v/cipher-parse.svg)](https://pypi.python.org/pypi/cipher-parse) ![example workflow](https://github.com/LightForm-group/cipher-parse/actions/workflows/test.yml/badge.svg) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LightForm-group/cipher-parse/HEAD)\n\n\nClick the Binder link above to try it out.\n\n## Acknowledgements\ncipher-parse was developed using funding from the [LightForm](https://lightform.org.uk/) EPSRC programme grant ([EP/R001715/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/R001715/1))\n\n\n<img src="https://lightform-group.github.io/wiki/assets/images/site/lightform-logo.png" width="150"/>\n',
    'author': 'aplowman',
    'author_email': 'adam.plowman@manchester.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
