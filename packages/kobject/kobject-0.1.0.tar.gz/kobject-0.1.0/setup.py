# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kobject']

package_data = \
{'': ['*']}

modules = \
['__init__']
setup_kwargs = {
    'name': 'kobject',
    'version': '0.1.0',
    'description': 'Know your object is a attribute type checker',
    'long_description': '```\n                       ▄▄          ▄▄                      \n▀████▀ ▀███▀          ▄██          ██                 ██   \n  ██   ▄█▀             ██                             ██   \n  ██ ▄█▀      ▄██▀██▄  ██▄████▄  ▀███  ▄▄█▀██ ▄██▀████████ \n  █████▄     ██▀   ▀██ ██    ▀██   ██ ▄█▀   ███▀  ██  ██   \n  ██  ███    ██     ██ ██     ██   ██ ██▀▀▀▀▀▀█       ██   \n  ██   ▀██▄  ██▄   ▄██ ██▄   ▄██   ██ ██▄    ▄█▄    ▄ ██   \n▄████▄   ███▄ ▀█████▀  █▀█████▀    ██  ▀█████▀█████▀  ▀████\n                                ██ ██                      \n                                ▀███                       By CenturyBoys\n                                \nKnow your object is a __init__ type validator for class and dataclass\n```\n\n## Usage\n\nKobject can be use inside default class declaration and with dataclasses. Kobject uses the ```__init__``` signature to check types.\n\n### Default classes\n\n```python\nfrom kobject import Kobject\n\nclass StubClass(Kobject):\n    a_int: int\n    a_bool: bool\n    \n    def __init__(\n        self,\n        a_int: int,\n        a_bool: bool\n    ):\n        self.a_int = a_int\n        self.a_bool = a_bool\n        self.__post_init__()\n\ninstance = StubClass(a_int=1, a_bool=True)\n```\nNotice that in the default class declaration you need to call ```self.__post_init__()``` at the end of the ```__init__``` declaration.\n\n\n### Dataclass\n\n```python\nfrom dataclasses import dataclass\nfrom kobject import Kobject\n\n@dataclass\nclass StubClass(Kobject):\n    a_int: int\n    a_bool: bool\n\ninstance = StubClass(a_int=1, a_bool=True)\n```\nBy default, dataclass calls ```self.__post_init__()``` at the end of the ```__init__``` declaration.\n\n\n### Exception\n\nKobject raises ```TypeError``` with all validation errors, that means it checks all your object\'s attributes before raising the ```TypeError```. Types like List and Tuple will have all their elements checked.\n\n```python\nfrom dataclasses import dataclass\nfrom kobject import Kobject\nfrom typing import List, Tuple\n\n@dataclass\nclass StubClass(Kobject):\n    a_list_int: List[int]\n    a_tuple_bool: Tuple[bool]\n\ninstance = StubClass(a_list_int=[1, "", 2, ""], a_tuple_bool=["", True])\n\nTraceback (most recent call last):\n  File "/snap/pycharm-community/312/plugins/python-ce/helpers/pydev/pydevconsole.py", line 364, in runcode\n    coro = func()\n  File "<input>", line 10, in <module>\n  File "<string>", line 5, in __init__\n  File "/home/marco/projects/kobject/kobject/__init__.py", line 67, in __post_init__\n    raise TypeError(message)\nTypeError: Validation Errors:\n    \'a_list_int\' : Wrong type! Expected (<class \'int\'>,) but giving <class \'str\'> on index 1\n    \'a_list_int\' : Wrong type! Expected (<class \'int\'>,) but giving <class \'str\'> on index 3\n    \'a_tuple_bool\' : Wrong type! Expected <class \'tuple\'> but giving <class \'list\'>\n    \'a_tuple_bool\' : Wrong type! Expected (<class \'bool\'>,) but giving <class \'str\'> on index 0\n```\n\n### Default value\n\nKobject supports default values and will check them before any validation, that means if you declare a ```a_bool: bool = None``` it will not raise an error.\n\n```python\nfrom dataclasses import dataclass\nfrom kobject import Kobject\n\nclass StubClass(Kobject):\n    a_bool: bool = None\n\n    def __init__(self, a_bool: bool = 2):\n        self.a_bool = a_bool\n        self.__post_init__()\n\n@dataclass\nclass StubDataClass(Kobject):\n    a_bool: bool = None\n```',
    'author': 'Marco Sievers de Almeida Ximit Gaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
