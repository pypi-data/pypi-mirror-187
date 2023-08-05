import json
import yaml
from kortical.api.project import Project
from kortical.api.environment import Environment


def get_config(format=None):
    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    # Get environment config from platform
    config = environment.get_config()
    if format == 'json':
        return json.loads(config)
    elif format == 'yaml' or format == 'yml':
        return yaml.safe_load(config)
    else:
        return config
    return config


def get_environment_name():
    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    return environment.name
