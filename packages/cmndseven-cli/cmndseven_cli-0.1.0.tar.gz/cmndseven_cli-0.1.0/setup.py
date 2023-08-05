# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmndseven_cli']

package_data = \
{'': ['*'],
 'cmndseven_cli': ['assets/bpmn-viewer.production.min.js',
                   'assets/bpmn-viewer.production.min.js',
                   'assets/bpmn-viewer.production.min.js',
                   'assets/bpmn-viewer.production.min.js',
                   'assets/bpmn-viewer.production.min.js',
                   'assets/bpmn-viewer.production.min.js',
                   'assets/index.js',
                   'assets/index.js',
                   'assets/index.js',
                   'assets/index.js',
                   'assets/index.js',
                   'assets/index.js',
                   'assets/instance.html',
                   'assets/instance.html',
                   'assets/instance.html',
                   'assets/instance.html',
                   'assets/instance.html',
                   'assets/instance.html',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/puppeteer.production.min.js.LICENSE.txt',
                   'assets/skeleton.html',
                   'assets/skeleton.html',
                   'assets/skeleton.html',
                   'assets/skeleton.html',
                   'assets/skeleton.html',
                   'assets/skeleton.html']}

install_requires = \
['chameleon>=3.10.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'generic-camunda-client>=7.18.0,<8.0.0',
 'setuptools>=66.1.0,<67.0.0']

entry_points = \
{'console_scripts': ['ccli = cmndseven_cli:main']}

setup_kwargs = {
    'name': 'cmndseven-cli',
    'version': '0.1.0',
    'description': 'Opinionated Camunda Platform 7 CLI',
    'long_description': '# ccli\n\nA placeholder project for to be opinionated Camunda Platform 7 CLI.\n\n## Usage\n\n```\nUsage: ccli [OPTIONS] COMMAND [ARGS]...\n\n  Opinionated Camunda Platform 7 CLI\n\nOptions:\n  --help  Show this message and exit.\n\n  render instance INSTANCE_ID [OUTPUT_PATH]\n```\n',
    'author': 'Asko Soukka',
    'author_email': 'asko.soukka@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datakurre/cmndseven-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
