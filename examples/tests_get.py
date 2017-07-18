from __future__ import print_function

import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Tests are retrieved by the run they are associated with
    # Get an example run using the Run ID
    auto_run = client.run(72215)

    # Get all tests for this run:
    tests = list(client.tests(auto_run))  # Expand the generator to a list
    print(len(tests))  # 40 tests

    test_1 = tests[0]
    print(test_1.title)  # Example Test Case Title
    print(test_1.status.label)  # Passed

    test_2 = tests[1]
    print(test_2.title)  # Example Test Case Title #2
    print(test_2.status.label)  # Failed

    # Get all tests with a status of `Failed` or 'Retest'
    failed_status = client.status('failed')
    retest_status = client.status('retest')
    failed_and_retest = list(client.tests(auto_run, with_status=[failed_status, retest_status]))

    print(len(failed_and_retest))  # 10

    # Get a test from its test id
    example_test = client.test(5792090)
    print(example_test.id)  # 5792090
    print(example_test.status.label)  # Failed
    print(example_test.type.name)  # Regression
    print(example_test.priority.name)  # Medium
    print(example_test.estimate)  # datetime.timedelta object -> datetime.timedelta(0, 4200)
    print(list(example_test.refs))  # ['REF001', 'REF002']

    # Since you cannot programatically add Tests through the API,
    # attempting to call `client.test()` will raise an exception rather
    # than returning an empty/new Test object
    try:
        client.test()
    except NotImplementedError as exc:
        # Not implemented directly. You must pass in int object
        print(str(exc))


if __name__ == "__main__":
    main()
