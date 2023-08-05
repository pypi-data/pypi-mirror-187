# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['timevec']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'timevec',
    'version': '0.0.0',
    'description': '',
    'long_description': '# timevec\n\nFunctions to create time vectors\n\n# Description\n\nTime has a periodic nature due to the rotation of the earth and the position of the sun.\nThis affects human behavior in various ways.\n\n- Seasonality ... periodicity in a year (seasonal distinction)\n- Daily periodicity ... periodicity in a day (distinction between day and night)\n- Day of the week ... periodicity in a week (distinction between weekdays and holidays)\n\nWhen dealing with these, it is desirable to vectorize with periodicity in mind.\nThat is, at 23:59 on a given day, it is desirable that the value is close to 00:00 on the next day.\nTo achieve this, the time is represented as a combination of cos and sin.\nThis is called a time vector.\n\n# Installation\n\n```sh\npip install timevec\n```\n\n# Usage\n\n```python\nimport timevec.numpy as tv\nimport datetime\ndt = datetime.datetime(2020, 1, 1, 0, 0, 0)\nvec = tv.year_vec(dt)\n# array([1., 0.])\n```\n\n# Functions\n\n- `timevec.numpy` provides functions that return numpy.ndarray.\n- `timevec.builtin_math` provides functions that return tuple of float.\n\n## year_vec\n\n```python\nyear_vec(dt: datetime.datetime)\n```\n\nCreate a time vector for a year.\nThis is a vector that has periodicity like seasonality.\n(Summer, Autumn, Winter, Spring)\n\n## month_vec\n\n```python\nmonth_vec(dt: datetime.datetime)\n```\n\nCreate a time vector for a month.\nThis is a vector that has periodicity in a month.\nYou can express periodicity such as the beginning of the month, the end of the month, and the salary day.\n\n## week_vec\n\n```python\nweek_vec(dt: datetime.datetime)\n```\n\nCreate a time vector for a week.\nThis is a vector that has periodicity in a week.\nYou can express periodicity such as weekdays and holidays.\n\n## day_vec\n\n```python\nday_vec(dt: datetime.datetime)\n```\n\nCreate a time vector for a day.\nThis is a vector that has periodicity in a day.\nYou can express periodicity such as morning, noon, and night.\n\n# License\n\nMIT\n',
    'author': 'kitsuyui',
    'author_email': 'kitsuyui@kitsuyui.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
