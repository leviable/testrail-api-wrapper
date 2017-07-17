from __future__ import print_function

import traw


def main():
    client = traw.Client()  # Credentials loaded through ENV vars

    # Get all available case types:
    case_types = client.case_types()  # Returns a case_types generator
    case_type_1 = next(case_types)
    print(case_type_1.name)  # Acceptance
    print(case_type_1.is_default)  # False
    print(isinstance(case_type_1, traw.models.CaseType))  # True

    case_type_2 = next(case_types)
    print(case_type_2.name)  # Accessibility
    print(case_type_2.is_default)  # False
    print(isinstance(case_type_2, traw.models.CaseType))  # True

    # etc

    # Get a specific case type by case_type_id
    specific_case_type = client.case_type(7)  # Corresponds to the `Other` CT
    print(specific_case_type.name)  # Other
    print(specific_case_type.is_default)  # True

    # Since you cannot programatically add Case Types through the API,
    # attempting to call `client.case_type()` will raise an exception rather
    # than returning an empty/new CaseType object
    try:
        client.case_type()
    except NotImplementedError as exc:
        print(str(exc))  # Not implemented directly. You must pass in int object


if __name__ == "__main__":
    main()
