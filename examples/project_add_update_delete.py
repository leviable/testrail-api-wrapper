import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Create a new project object
    new_project = client.project()
    new_project.name = "ACME Contract Testing"
    new_project.announcement = "For testing associated with the Acme Contract"
    new_project.show_announcement = True
    new_project.suite_mode = 1  # Single Suite mode

    # Add the project to testrail, replacing it with the Milestone returned
    # from the TestRail API.
    active_project = client.add(new_project)
    project_id = active_project.id

    # Verify some parameters
    assert active_project.name == "ACME Contract Testing"
    assert active_project.announcement == "For testing associated with the Acme Contract"
    assert active_project.is_completed is False

    # Lets say the project is now complete.
    # Update the name, announcement, and completion status
    active_project.name = "ACME Contract Testing - Complete"
    active_project.announcement = ("For testing associated with the Acme Contract,"
                                   "completed 2018/01/02")
    active_project.is_completed = True

    # POST the updated project to Testrail, replacing it with the Project returned
    # from the API
    closed_project = client.update(active_project)

    assert closed_project.name == "ACME Contract Testing - Complete"
    assert closed_project.announcement == ("For testing associated with the Acme Contract,"
                                           "completed 2018/01/02")
    assert closed_project.is_completed is True

    # Lets say its now a few years later, and we want to remove this old project
    # NOTE: your user must have admin privs to delete a project
    old_project = client.project(project_id)
    client.delete(old_project)


if __name__ == "__main__":
    main()
