from __future__ import print_function

import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Get all priorities
    priorities = client.priorities()  # Returns a models.Priority generator
    priority_1 = next(priorities)
    print(priority_1.name)  # Low
    priority_2 = next(priorities)
    print(priority_2.name)  # Medium
    priority_3 = next(priorities)
    print(priority_3.name)  # High
    priority_4 = next(priorities)
    print(priority_4.name)  # Critical

    # Given a priority ID, you can get the priority object
    priority_from_api = client.priority(1)
    print(priority_from_api.name)  # Low

    # Since you cannot programatically add priorities through the API,
    # attempting to call `client.priority()` will raise an exception rather
    # than returning an empty/new Priority object
    try:
        client.priority()
    except NotImplementedError as exc:
        print(str(exc))  # Not implemented directly. You must pass in int object


if __name__ == "__main__":
    main()
