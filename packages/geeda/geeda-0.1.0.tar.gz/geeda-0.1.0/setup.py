# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['geeda', 'geeda.column', 'geeda.dataframe']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.15.2,<7.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'scipy>=1.9.1,<2.0.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'geeda',
    'version': '0.1.0',
    'description': 'General EDA Framework for Pandas DataFrames',
    'long_description': '# geeda\nPronounced ghee-dah or jee-dee-aye \\\nGee.D.A, GEneral EDA: General EDA (Exploratory Data Analysis) Framework for Pandas DataFrames\n\n## Where to get it\nThe source code is currently hosted on GitHub at:\nhttps://github.com/jjz17/geeda\n\nBinary installers for the latest released version are available at the [Python\nPackage Index (PyPI)](https://pypi.org/project/geeda/).\n\n```bash\n# PyPI\npip install geeda\n```\n\n## EDA Workflow using Geeda\n1. Create the `Geeda()` object by passing in the dataframe you wish to explore/analyze\n2. Call the `apply()` function with the desired arguments (EDA functions that you wish to apply)\n3. Enjoy an organized and simple output of the EDA results\n\n\n# Technologies Used\n* Python3\n* Poetry (dependency management, publishing library)\n* Docker (containerization of services and tests)\n* Git/GitHub (version control, CI/CD)\n* Pre-commit (hooks for improved code quality)\n* Black (code formatting)\n',
    'author': 'Jason Zhang',
    'author_email': 'jasonjzhang17@gmail.com',
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
