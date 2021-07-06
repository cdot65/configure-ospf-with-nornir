from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from rich import print

nr = InitNornir(config_file="config.yaml")

def configure_ospf(task):

    # pass in variables from inventory file
    data = {}
    data['ospf'] = task.host['ospf']
    print(data)

    # execute our task by templating our variables through a Jinja2 template to produce config
    # push and commit
    response = task.run(
        task=pyez_config, template_path='templates/ospf.j2', template_vars=data, data_format='set')
    if response:
        diff = task.run(pyez_diff)
    if diff:
        task.run(task=pyez_commit)


if __name__ == "__main__":
    response = nr.run(task=configure_ospf)
    print_result(response)
