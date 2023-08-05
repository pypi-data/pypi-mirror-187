# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['livingdocs']

package_data = \
{'': ['*']}

install_requires = \
['behave>=1.2.6,<2.0.0']

entry_points = \
{'console_scripts': ['aidee-living-docs = livingdocs.cli:main',
                     'behave2sphinx = '
                     'livingdocs.create_sphinx_feature_file_page:main',
                     'behave2sphinx-all = '
                     'livingdocs.create_sphinx_feature_file_page:process_files_in_current_directory',
                     'createtracepage = livingdocs.create_trace_page:main',
                     'userneeds2sphinx = '
                     'livingdocs.create_userneeds_page:main']}

setup_kwargs = {
    'name': 'aidee-living-docs',
    'version': '1.0.3',
    'description': 'Helpers for generating living documentation with Sphinx and Behave',
    'long_description': '# Aidee Living Documentation Helpers\n\n[![PyPI](https://img.shields.io/pypi/v/aidee-living-docs.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/aidee-living-docs.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/aidee-living-docs)][python version]\n[![License](https://img.shields.io/pypi/l/aidee-living-docs)][license]\n\n[![Tests](https://github.com/aidee-health/aidee-living-docs/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/aidee-living-docs/\n[status]: https://pypi.org/project/aidee-living-docs/\n[python version]: https://pypi.org/project/aidee-living-docs\n[tests]: https://github.com/aidee-health/aidee-living-docs/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Helper functions to generate living documentation with Sphinx and Behave\n- Type safe code using [mypy](https://mypy.readthedocs.io/) for type checking\n\n## Requirements\n\n- Python 3.9-3.11\n\n## Installation\n\nYou can install _Aidee Living Documentation_ via [pip]:\n\n```console\n$ pip install aidee-living-docs\n```\n\nThis adds `aidee-living-docs` as a library, but also provides the CLI application with the same name.\n\n## Using the application from the command line\n\nThe application also provides a CLI application that is automatically added to the path when installing via pip.\n\nOnce installed with pip, type:\n\n```\naidee-living-docs --help\n```\n\nTo see which options are available.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[file an issue]: https://github.com/aidee-health/aidee-living-docs/issues\n[pip]: https://pip.pypa.io/\n\n## Credits\n\nThis project has been heavily inspired by [Bluefruit](https://github.com/bluefruit/LivingDocumentationHelpers)\n\n<!-- github-only -->\n\n[license]: https://github.com/aidee-health/aidee-living-docs/blob/main/LICENSE\n[contributor guide]: https://github.com/aidee-health/aidee-living-docs/blob/main/CONTRIBUTING.md\n',
    'author': 'Aidee Health AS',
    'author_email': 'hello@aidee.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aidee-health/aidee-living-docs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
