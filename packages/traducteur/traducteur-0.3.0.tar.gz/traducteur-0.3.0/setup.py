# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traducteur',
 'traducteur.context',
 'traducteur.exceptions.tasks',
 'traducteur.managers',
 'traducteur.models.base',
 'traducteur.models.nosql',
 'traducteur.tasks.base',
 'traducteur.tasks.task',
 'traducteur.tasks.worker']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'traducteur',
    'version': '0.3.0',
    'description': 'Traducteur is the middle man to handle data',
    'long_description': '# Traducteur\nTraducteur is a database model manager and task sheduler which aims to make developing basic app with database models and tasks faster and easier.\n\n\n<div align="center">\n    <img src="https://img.shields.io/pypi/v/traducteur"/>\n    <img src="https://img.shields.io/pypi/dm/traducteur"/>\n    <img src="https://img.shields.io/pypi/pyversions/traducteur"/>\n</div>\n\n## Requirements\n- `python ^3.8`\n- `pydantic ^1.10.4`\n\n__For mongo db management:__\n- `pymongo ^4.3.3`\n\n__For task queueing or redis model management:__\n- `redis-py ^4.4.2`\n\n## The idea\n\n### Context managers\n```python\nwith BaseContext(connection_string) as db:\n    return db.get()\n```\n\n### Model managers\nModel managers use context managers\n```python\nmanager = BaseModelManager(connection_string)\nresult = manager.find_one(query)\nresult = manager.delete(query)\n```\n\n### Models\nModels use model managers\n```python\nclass User(BaseDatabaseModel):\n    username: str\n    fname: str\n    lname: str\n    email: str\n    \nuser = User(\n    username=\'johndoe\',\n    fname=\'John\',\n    lname=\'Doe\',\n    email=\'john.doe@mail.com\'\n)\n\n\'\'\'\n    Easy create, save, update and delete\n\'\'\'\nuser = User(\n    username=\'johndoe\',\n    fname=\'John\',\n    lname=\'Doe\',\n    email=\'john.doe@mail.com\'\n)\n\n# saving the model\nuser = user.save()\n\n# saving also updates the model\nuser.lname = \'Joe\'\nuser = user.save()\n\n# getting a model by its ID from the database\nuser = User.get(user_id)\n\n# deleting a model from the database\ndeleted_user = user.delete()\n```\n\n### Tasks\nTasks use models\n```python\n# in a program\ndef my_func(a: int, b: int) -> int:\n  return a + b\n\ntask = BaseTask(action=my_func)\ntask.queue(a=8, b=3)\n\n###############\n# in a worker #\ntask.digest() #\n###############\n\n# some time later\nresult = task.result()\n```\n\n### Chain tasks\nTasks can be chained together for larger workloads\n```python\ndef double(number: int):\n    return {\n        \'number\': number * 2\n    }\n\n# make tasks\none = BaseTask(action=double)\ntwo = BaseTask(action=double)\nthree = BaseTask(action=double)\n\n# chain tasks\ntwo.set_parent(one)\nthree.set_parent(two)\n\n# queue parent task\none.queue(number=2)\n\n###############\n# in a worker #\none.digest()  #\n###############\n\n# some time later\nresult = one.result()\nassert result == 8, "Should be 8 as 2*2*2 == 8"\n```\n\n\n## Available functionality\n\n### Context managers\n- MongoContext\n- SQLite3Context\n\n\n### Model managers\n- MongoModelManager\n\n### Models\n- BaseMongoModel\n- BaseRedisModel\n\n### Tasks\n- RedisTask\n\n# Todo / in progress\n\n### Models\n- [ ] SQLite support\n\n### Tasks\n- [ ] Chain tasks\n    - [x] Redis\n    - [ ] Mongo\n    - [ ] SQL\n- [ ] Task worker\n  \t- [ ] Single Process\n    - [ ] Multi Process\n- [ ] RabbitMQ task\n\n### Managers\n- [ ] SQLite manager\n\n\n# Tests\n\nTests can be found in the `tests` folder. They use pythons `unittest` and can be run with:\n```\npython3 -m unittest path/to/test.py\n```\n\n### Available tests\n- Redis task\n    - Basic functions\n    - Chaining',
    'author': 'Seppe De Langhe',
    'author_email': 'seppedelanghe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
