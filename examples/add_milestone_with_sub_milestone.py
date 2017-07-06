from datetime import datetime as dt

import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Locate the project you will be adding milestones to
    project = client.project(15)

    # Create the parent milestone
    new_parent_ms = client.milestone()  # Creates a new, empty milestone object
    new_parent_ms.name = "{0}'s Yearly Test Results".format(project.name)
    new_parent_ms.description = "{0}'s testing results for the year".format(project.name)
    new_parent_ms.start_on = dt(year=2018, month=1, day=1)  # Start on 2018/01/01
    new_parent_ms.due_on = dt(year=2018, month=12, day=31)  # Due on 2018/12/31

    # Associate this milestone with a project
    new_parent_ms.project = project

    # Add the new milestone to TestRail, replacing it with the Milestone returned
    # from the TestRail API.
    parent_ms = client.add(new_parent_ms)
    assert isinstance(parent_ms, traw.models.Milestone)

    # Create a sub milestone for the first quarter of 2018
    new_sub_ms = client.milestone()  # Creates a new, empty milestone object
    new_sub_ms.name = "{0}'s 1st Quarter Test Results".format(project.name)
    new_sub_ms.description = "{0}'s testing results for the first quarter".format(project.name)
    new_sub_ms.start_on = dt(year=2018, month=1, day=1)  # Start on 2018/01/01
    new_sub_ms.due_on = dt(year=2018, month=3, day=31)  # Due on 2018/03/31

    # Associate this milestone with a project
    new_sub_ms.project = project

    # Add the parent milestone, transforming this into a sub_milestone object
    new_sub_ms = new_sub_ms.add_parent(parent_ms)

    # Add the new milestone to TestRail, replacing it with the Milestone returned
    # from the TestRail API.
    sub_ms = client.add(new_sub_ms)
    assert isinstance(sub_ms, traw.models.SubMilestone)

    # The sub_ms's parent should match the one we created
    assert sub_ms.parent.id == parent_ms.id


if __name__ == "__main__":
    main()
