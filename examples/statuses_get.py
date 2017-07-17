from __future__ import print_function

import traw
from traw.exceptions import TRAWClientError


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Get all Statuses
    statuses = client.statuses()  # Returns a models.Status generator
    status_1 = next(statuses)
    print(status_1.name)      # passed
    print(status_1.label)     # Passed
    status_2 = next(statuses)
    print(status_2.name)      # blocked
    print(status_2.label)     # Blocked
    status_3 = next(statuses)
    print(status_3.name)      # untested
    print(status_3.label)     # Untested
    status_4 = next(statuses)
    print(status_4.name)      # retest
    print(status_4.label)     # Retest
    status_5 = next(statuses)
    print(status_5.name)      # failed
    print(status_5.label)     # Failed
    status_6 = next(statuses)
    print(status_6.name)      # custom_status_auto_passed
    print(status_6.label)     # Passed-Automation

    # etc

    # Given a status ID, you can get the status object
    failed_auto_st = client.status(7)
    print(failed_auto_st.name)   # custom_status_auto_failed
    print(failed_auto_st.label)  # Failed-Automation

    # Given a status label, you can get the status object
    # By default it ignores case
    blocked_auto_st = client.status('blocked-automation')
    print(blocked_auto_st.name)   # custom_status_auto_blocked
    print(blocked_auto_st.label)  # Blocked-Automation

    # You can specify strict casing if necessary:
    try:
        client.status('blocked-automation', strict=True)
    except TRAWClientError as exc:
        # Could not locate a models.Status with label of blocked-automation
        print(str(exc))

    strict_status = client.status('Blocked-Automation', strict=True)
    print(strict_status.name)   # custom_status_auto_blocked
    print(strict_status.label)  # Blocked-Automation

    # Since you cannot programatically add statuses through the API,
    # attempting to call `client.status()` will raise an exception rather
    # than returning an empty/new Status object
    try:
        client.status()
    except NotImplementedError as exc:
        print(str(exc))  # Not implemented directly. You must pass in int object


if __name__ == "__main__":
    main()
