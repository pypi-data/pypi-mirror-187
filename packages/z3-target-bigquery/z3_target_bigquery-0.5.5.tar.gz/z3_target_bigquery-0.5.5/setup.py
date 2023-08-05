# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_bigquery', 'target_bigquery.tests']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['google-cloud-bigquery[bqstorage]>=3.4.1,<4',
 'google-cloud-storage>=2.7.0,<3',
 'grpcio-status[grpc]>=1.51.1,<2',
 'grpcio-tools>=1.51.1,<2',
 'orjson>=3.7.2,<4',
 'requests>=2.25.1',
 'singer-sdk>=0.16.0',
 'tenacity>=8.0.1,<9']

entry_points = \
{'console_scripts': ['target-bigquery = '
                     'target_bigquery.target:TargetBigQuery.cli']}

setup_kwargs = {
    'name': 'z3-target-bigquery',
    'version': '0.5.5',
    'description': 'z3-target-bigquery is a Singer target for BigQuery. It supports storage write, GCS, streaming, and batch load methods. Built with the Meltano SDK.',
    'long_description': 'None',
    'author': 'Alex Butler',
    'author_email': 'butler.alex2010@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/z3z1ma/target-bigquery',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
