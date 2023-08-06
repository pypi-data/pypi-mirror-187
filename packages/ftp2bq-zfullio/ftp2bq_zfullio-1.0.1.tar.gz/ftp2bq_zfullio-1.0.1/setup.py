# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ftp2bq_zfullio']

package_data = \
{'': ['*']}

install_requires = \
['bq-easy-zfullio>=1,<2',
 'loguru>=0.6,<0.7',
 'openpyxl>=3.0,<4.0',
 'pandas>=1.5,<2.0',
 'paramiko>=3,<4',
 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'ftp2bq-zfullio',
    'version': '1.0.1',
    'description': '',
    'long_description': '# (S)FTP to BQ\n\nЭкспорт файлов с FTP и SFTP в BigQuery',
    'author': 'viktor',
    'author_email': 'vi.dave@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
