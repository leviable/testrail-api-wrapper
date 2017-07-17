from __future__ import print_function

import traw
from traw.exceptions import TRAWClientError


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # TestRail returns config groups based on project, with each config group
    # containing specific configs. To get a config group, you must first get
    # the corresponding project by project ID:
    automation_project = client.project(15)

    # Get all config groups for our project. This method returns a generator, so
    # Use `list` to get a complete list of config groups
    config_groups = list(client.config_groups(automation_project))
    print(len(config_groups))  # 1

    config_group = config_groups[0]
    print(str(config_group))  # ConfigGroup-4
    print(config_group.name)  # 'Supported Browsers'
    print(config_group.project)  # Project-15
    print(len(list(config_group.configs)))  # 2 configs

    # Get/examine configs for each config group
    configs = config_groups[0].configs
    config_1 = next(configs)
    print(config_1.name)  # Chrome
    print(config_1.config_group)  # ConfigGroup-4, a reference back to the CG
    print(config_1.project)  # Project-15, a reference back to the project

    config_2 = next(configs)
    print(config_2.name)  # Firefox
    print(config_2.config_group)  # ConfigGroup-4, a reference back to the CG
    print(config_2.project)  # Project-15, a reference back to the project

    # You can retrieve a ConfigGroup  using project + config group ID
    print(client.config_group(automation_project, 4))  # ConfigGroup-4

    # You can create new config groups and configs and add them to TestRail
    new_config_group = client.config_group()  # Returns a new/empty config group

    # Set the name and associate it with a project
    new_config_group.name = "Supported Operating Systems"
    new_config_group.project = automation_project

    # Add the new config group to TestRail, and collect the returned object
    created_config_group = client.add(new_config_group)

    # Note that the returned config group matches the one you added and now has
    # and ID, but no associated configs
    print(created_config_group.name == new_config_group.name)  # True
    print(created_config_group.id)  # 5
    print(list(created_config_group.configs))  # []

    # Create new configs, associate them with a config group, and add them to TR
    new_config_1 = client.config()
    new_config_1.name = "Windows"
    new_config_1.config_group = created_config_group
    created_config_1 = client.add(new_config_1)
    print(created_config_1)  # Windows

    new_config_2 = client.config()
    new_config_2.name = "Linux"
    new_config_2.config_group = created_config_group
    created_config_2 = client.add(new_config_2)
    print(created_config_2)  # Linux

    new_config_3 = client.config()
    new_config_3.name = "mac OS"
    new_config_3.config_group = created_config_group
    created_config_3 = client.add(new_config_3)
    print(created_config_3)  # mac OS

    # Re-acquire the config group from the TestRail API
    updated_config_group = client.config_group(created_config_group.project,
                                               created_config_group.id)

    # Note that it now has three configs:
    cg_configs = list(updated_config_group.configs)
    print(cg_configs)  # [Config-25, Config-26, Config-24]

    print(cg_configs[0].name)  # Linux
    print(cg_configs[1].name)  # mac OS
    print(cg_configs[2].name)  # Windows

    # Should you need to update a config group or config
    to_be_updated_config = cg_configs[0]
    to_be_updated_config.name = "Linux: Ubuntu"  # From 'Linux' to 'Linux: Ubuntu'
    updated_config = client.update(to_be_updated_config)
    print(updated_config.name)  # 'Linux: Ubuntu'

    # Re-acquire the config group from the TestRail API
    updated_config_group = client.config_group(updated_config_group.project,
                                               updated_config_group.id)

    cg_configs = updated_config_group.configs
    print(next(cg_configs).name)  # Linux: Ubuntu
    print(next(cg_configs).name)  # mac OS
    print(next(cg_configs).name)  # Windows

    # Finally, should you want to delete a config/config group
    client.delete(updated_config_group)

    # And it is no longer in TestRail
    try:
        client.config_group(updated_config_group.project, updated_config_group.id)
    except TRAWClientError as exc:
        # Could not locate a models.ConfigGroup with id of 4 for project with ID 15
        print(str(exc))


if __name__ == "__main__":
    main()
