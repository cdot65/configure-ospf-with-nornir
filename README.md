# Juniper Configure OSPF

This example will show how to use the PyEZ plugin for Nornir to

1. build a NETCONF connection to a remote device
2. configure OSPF
3. close the connection

## 🚀 Workflow

We have provided a [Poetry](https://python-poetry.org/docs/) lock file to make life simple when managing Python packages and virtual environments. Within the virtual vironment, there will be a package called [Invoke](http://www.pyinvoke.org/) that will help us run our script with a simple command.

The workflow will look like this:

1. Install Poetry (one-time operation)
2. Have Poetry install your Python packages in a virtual environment (one-time operation)
3. Activate your new virtual environment with Poetry
4. Run locally or within a container using the Invoke package

### 🐍 Create and Activate your Python environment (one time operation)

1. install poetry package to manage our Python virtual environment 

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

2. install our Python dependencies 

```sh
poetry install
```

3. activate your Python virtual environment

```sh
poetry shell
```

### Executing the script

1. run your Nornir script locally

```sh
cd files/nornir
python app.py
```

### Using Docker

1. build the container image with

```sh
invoke build
```

2. run the Nornir script within the container

```sh
invoke nornir
```

## ⚙️ How it works

Let's take a second to do a nice John Madden play-by-play on this script:

### Importing the functionality of PyEZ and Nornir into our script

```python
from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from rich import print
```

- We need to import the PyEZ methods from Nornir's PyEZ plugin into our script
- `InitNornir` will import the core functionality of Nornir
- `rich` will make things pretty when we print the output
- `print_result` will enable us to print the results of the task

### Defining parameters

```python
nr = InitNornir(config_file="config.yaml")
```

- `nr` is created by instantiation the `InitNornir` class and passing our config file into it

### `configure_ospf` function

```python
def configure_ospf(task):

    # pass in variables from inventory file
    data = {}
    data['ospf'] = task.host['ospf']
    print(data)
```

- we pass the `task` object as a parameter into the `configure_ospf` function
  - this will give us access to our device's `ospf` object (defined in the `inventory/inventory.yaml` file)
- create a new object called `data` and setting it equal to the key/value pairs of `ospf` object

```python
    # execute our task by templating our variables through a Jinja2 template to produce config
    # push and commit
    response = task.run(
        task=pyez_config, template_path='templates/ospf.j2', template_vars=data, data_format='set')
```

- create a new object called `response` and set it equal to the result of our task
- the `run` method was imported when we created the `task` object from the `InitNornir` class
- within `run`
  - we pass the `task` as a `pyez_config`
  - define the path to our Jinja2 template
  - pass our variables
  - declare that we want to send the box config in the format of `set` commands

```python
    if response:
        diff = task.run(pyez_diff)
    if diff:
        task.run(task=pyez_commit)
```

- if there is a response, print the diff to the screen
- if a diff exists, commit our changes

### Execute our function

```python
if __name__ == "__main__":
    response = nr.run(task=configure_ospf)
    print_result(response)
```

- call our function within Python's `if __name__ == "__main__":` standard conditional
- print the reponse to the screen

## 📸 Screenshot

![app.py](./files/images/screenshot.png)

## 📝 Additional Notes

### 🐍 Python

You are *strongly* recommended to using a Python Virtual Environment any and everywhere possible. You can really mess up your machine if you're too lazy and say "ehh, that seems like it's not important". It is. If it sounds like I'm speaking from experience, I'll never admit to it.

If you're interested in learning more about setting up Virtual Environments, I encourage you to read a few blogs on the topic. A personal recommendation would be

- [Poetry](https://python-poetry.org/docs/)
- [Digital Ocean (macOS)](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos)
- [Digital Ocean (Windows 10)](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10)

### 🐳 Docker

If you are unsure if Docker is installed on your computer, then it's probably safe to suggest that it's not. If you're interested in learning more about the product, I encourage you to read a few blogs on the topic. A personal recommendation would be [Digital Ocean](https://www.digitalocean.com/community/tutorial_collections/how-to-install-and-use-docker#:~:text=Docker%20is%20an%20application%20that,on%20the%20host%20operating%20system.)

Some of the goodies placed in the `docker` folder are not relevant to our use case with Python. Feel free to delete them as you see fit, I simply wanted to share with you my Docker build process for all Juniper automation projects (including those based on Ansible). The world is your oyster and I won't judge you on whatever direction you take.

### 📝 Dependencies

Refer to the file located at [files/docker/requirements.txt](files/docker/requirements.txt)
