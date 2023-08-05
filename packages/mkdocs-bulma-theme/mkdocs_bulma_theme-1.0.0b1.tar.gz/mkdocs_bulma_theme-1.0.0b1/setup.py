# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs-bulma-theme']

package_data = \
{'': ['*'],
 'mkdocs-bulma-theme': ['assets/js/*',
                        'assets/sass/*',
                        'assets/sass/bulma/*',
                        'assets/sass/bulma/sass/base/*',
                        'assets/sass/bulma/sass/components/*',
                        'assets/sass/bulma/sass/elements/*',
                        'assets/sass/bulma/sass/form/*',
                        'assets/sass/bulma/sass/grid/*',
                        'assets/sass/bulma/sass/helpers/*',
                        'assets/sass/bulma/sass/layout/*',
                        'assets/sass/bulma/sass/utilities/*',
                        'assets/sass/fontawesome6/*',
                        'img/*',
                        'webfonts/*']}

entry_points = \
{'mkdocs.themes': ['bulma = mkdocs-bulma-theme']}

setup_kwargs = {
    'name': 'mkdocs-bulma-theme',
    'version': '1.0.0b1',
    'description': 'Another theme for Mkdocs leveraging use of Bulma css framework.',
    'long_description': '# Mkdocs Bulma Theme\n\nAnother theme for Mkdocs leveraging use of Bulma css framework.\n\nLook at the [documentation](https://daniele-tentoni.github.io/mkdocs-bulma-theme).\n\nInstall using `pip install mkdocs-bulma-theme`.\n\nLook at the [Mkdocs Bulma Classes Plugin](https://github.com/Daniele-Tentoni/mkdocs-bulma-classes-plugin) too.\n',
    'author': 'Daniele Tentoni',
    'author_email': 'daniele.tentoni.1996@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
