# pyhassbian [![Build Status](https://travis-ci.com/ludeeus/pyhassbian.svg?branch=master)](https://travis-ci.com/ludeeus/pyhassbian) [![PyPI version](https://badge.fury.io/py/pyhassbian.svg)](https://badge.fury.io/py/pyhassbian)

_A python module to interact with hassbian-config._

## Install

```bash
pip install pyhassbian
```

### Verify that hassbian-config is installed

```python
import pyhassbian
pyhassbian.is_installed()
# Sample output: True
```

### Get a list of all available suites

```python
import pyhassbian
print(pyhassbian.get_suites())
# Sample output: ['hue', 'samba', 'homeassistant']
```

### Get the version number of hassbian-config

```python
import pyhassbian
print(pyhassbian.get_version())
# Sample output: '0.9.3'
```

### Install or upgrade a suite with hassbian-config

```python
import pyhassbian
pyhassbian.manage_suite('install', 'hue')
pyhassbian.manage_suite('upgrade', 'homeassistant', version='0.80.3')
pyhassbian.manage_suite('upgrade', 'hassbian-script', dev=True)
```

### Upgrade the base OS

```python
import pyhassbian
pyhassbian.os_upgrade()
```