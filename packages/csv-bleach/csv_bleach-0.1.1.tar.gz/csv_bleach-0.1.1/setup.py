# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_bleach']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.1.0,<6.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['bleach = csv_bleach.main:cli']}

setup_kwargs = {
    'name': 'csv-bleach',
    'version': '0.1.1',
    'description': 'clean CSVs',
    'long_description': '# clean your CSVs!\n\nThis command line tool cleans CSV files by:\n1. detecting the encoding and converting it to utf-8\n2. detecting the delimiter and safely converting it to a comma\n3. casting all variables to json form, i.e. integers, floats, booleans, string or null.\n\n\nA pypi build is not available yet so:\n* checkout the code \n* build it `poetry build`\n* and run like `poetry run bleach my-data.csv`\n\nThe only option is the output file name, by default it will be your original file name with `.scsv` extension.\n\nYou will now be able to parse your CSV safely with a simple script like:\n\n```python\nimport json\n\n\ndef parse_row(text: str) -> list:\n    return json.loads(f"[{text}]")\n\n\nwith open("my-data.scsv") as f:\n    header, *rows = map(parse_row, f)\n    for row in rows:\n        print(dict(zip(header, row)))\n```\n',
    'author': 'George Burton',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
