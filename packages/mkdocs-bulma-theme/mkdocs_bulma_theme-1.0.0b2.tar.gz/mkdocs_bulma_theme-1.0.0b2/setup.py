# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_bulma_theme']

package_data = \
{'': ['*'],
 'mkdocs_bulma_theme': ['css/*',
                        'img/*',
                        'js/*',
                        'sass/*',
                        'sass/bulma/*',
                        'sass/bulma/sass/base/*',
                        'sass/bulma/sass/components/*',
                        'sass/bulma/sass/elements/*',
                        'sass/bulma/sass/form/*',
                        'sass/bulma/sass/grid/*',
                        'sass/bulma/sass/helpers/*',
                        'sass/bulma/sass/layout/*',
                        'sass/bulma/sass/utilities/*',
                        'sass/fontawesome6/scss/*',
                        'webfonts/*']}

entry_points = \
{'mkdocs.themes': ['bulma = mkdocs_bulma_theme']}

setup_kwargs = {
    'name': 'mkdocs-bulma-theme',
    'version': '1.0.0b2',
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
