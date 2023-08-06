# Redis-simple

Redis-simple is a Python package that contains handy functions for interacting with Redis Library. 

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install RedisSimple like below. 
Rerun this command to check for and install  updates .
```bash
pip install redissimple
```

## Usage
Features:
* functions.get (tenant_id, entity_name, entity_id)  --> Get the data stored for provided key in the Redis Cache.
* functions.set    --> Set the key value pair in the Redis cache
* functions.remove      --> Remove the key from Redis Cache

##
How to create distribution
* Delete existing dist folder on project root directory
* Execute below command on project root directory
** python3 setup.py sdist

How to upload distribution to pypi
python3 -m twine upload --repository pypi dist/*

#### Demo of some of the features:
```python

```
