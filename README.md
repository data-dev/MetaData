<p align="left">
<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt=“DAI-Lab” />
<i>An open source project from Data to AI Lab at MIT.</i>
</p>

[![Development Status](https://img.shields.io/badge/Development%20Status-2%20--%20Pre--Alpha-yellow)](https://pypi.org/search/?c=Development+Status+%3A%3A+2+-+Pre-Alpha)
[![PyPI Shield](https://img.shields.io/pypi/v/metad.svg)](https://pypi.python.org/pypi/metad)
[![Github Actions Shield](https://img.shields.io/github/workflow/status/data-dev/MetaData/Run%20Tests)](https://github.com/data-dev/MetaData/actions)
[![Coverage Status](https://codecov.io/gh/data-dev/MetaData/branch/master/graph/badge.svg)](https://codecov.io/gh/data-dev/MetaData)

<p style="margin-bottom:1em;"></p>

# MetaData

This project aims to formally define a JSON schema which captures the structure of a relational database.

- JSON Schema: https://data-dev.github.io/MetaData/schema.html
- Documentation: https://data-dev.github.io/MetaData
- Homepage: https://github.com/data-dev/MetaData
- License: [MIT](LICENSE)

# Install

## Requirements

**MetaData** has been developed and tested on [Python 3.5, 3.6, 3.7 and 3.8](https://www.python.org/downloads/)

Also, although it is not strictly required, the usage of a [virtualenv](https://virtualenv.pypa.io/en/latest/)
is highly recommended in order to avoid interfering with other software installed in the system
in which **MetaData** is run.

## Install with pip

The easiest and recommended way to install **MetaData** is using [pip](
https://pip.pypa.io/en/stable/):

```bash
pip install metad
```

This will pull and install the latest stable release from [PyPi](https://pypi.org/).

If you want to install from source or contribute to the project please read the
[Contributing Guide](https://hdi-project.github.io/MetaData/contributing.html#get-started).

# Quickstart

In this short tutorial we will guide you through a series of steps that will help you
getting started with **MetaData**.

## Creating Metadata Objects

You can also help create Metadata objects from scratch. The following code will create a
`MetaData` object, add a table, and then save it to a JSON file.

```python3
from metad import MetaData

metadata = MetaData()

metadata.add_table({
    "id": "users",
    "name": "users",
    "primary_key": "id",
    "fields": [
        {"name": "id", "data_type": "id"},
        {"name": "name", "data_type": "text"}
    ],
})
```

Then, to export this object to a JSON file, you can run the following:

```python3
metadata.to_json("your_metadata.json")
```

## Validating JSON Files

The core functionality of this library is to validate JSON files. The following code will load
the metadata file for the `hello_world` dataset and validate it.

```python3
from metad import MetaData

metadata = MetaData.from_json("your_metadata.json")
metadata.validate()
```

# What's next?

For more details about **MetaData** and all its possibilities and features, please check the
[documentation site](https://data-dev.github.io/MetaData/).
