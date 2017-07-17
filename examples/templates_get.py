from __future__ import print_function

import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Templates are retrieved by the project they are associated with
    automation_project = client.project(15)

    # Get all available templates:
    templates = client.templates(automation_project)  # Returns a templates generator
    template_1 = next(templates)
    print(template_1.name)  # Default Test Case
    print(template_1.is_default)  # True
    print(isinstance(template_1, traw.models.Template))  # True

    template_2 = next(templates)
    print(template_2.name)  # Automation Test Case
    print(template_2.is_default)  # False
    print(isinstance(template_2, traw.models.Template))  # True

    # etc

    # Since you can only retrieve templates based on project,
    # attempting to call `client.templates()` will raise an exception
    try:
        client.templates()
    except NotImplementedError as exc:
        # Not implemented directly. You must pass in models.Project or int object
        print(str(exc))


if __name__ == "__main__":
    main()
