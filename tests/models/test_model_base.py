import pytest

from traw.models import Priority, Result, Status


@pytest.fixture()
def status1a(client):
    yield Status(client, {'id': 1})


@pytest.fixture()
def status1b(client):
    yield Status(client, {'id': 1})


@pytest.fixture()
def status1c(client):
    yield Status(client, {'id': 1, 'foo': 'bar'})


@pytest.fixture()
def status2(client):
    yield Status(client, {'id': 2})


@pytest.fixture()
def priority1(client):
    yield Priority(client, {'id': 1})


def test___eq___ids_match(status1a, status1b):
    assert (status1a == status1b) is True


def test___eq___ids_dont_match(status1a, status2):
    assert (status1a == status2) is False


def test___eq___ids_match_commutative(status1a, status1b):
    assert (status1b == status1a) is True


def test___eq___ids_dont_match_commutative(status1a, status2):
    assert (status2 == status1a) is False


def test___eq___hashes_dont_match(status1a, status1c):
    assert (status1a == status1c) is False


def test___eq___types_dont_match(status1a, priority1):
    assert (status1a == priority1) is False


def test___eq___hashes_change_as_object_changes(client):
    result1 = Result(client)
    result2 = Result(client)
    assert (result1 == result2) is True

    result1.comment = "mock comment a"

    assert (result1 == result2) is False

    result2.comment = "mock comment b"

    assert (result1 == result2) is False

    result2.comment = "mock comment a"

    assert (result1 == result2) is True


def test___ne___ids_match(status1a, status1b):
    assert (status1a != status1b) is False


def test___ne___ids_dont_match(status1a, status2):
    assert (status1a != status2) is True


def test___ne___ids_match_cummutative(status1a, status1b):
    assert (status1b != status1a) is False


def test___ne___ids_dont_match_cummutative(status1a, status2):
    assert (status2 != status1a) is True


def test___ne___hashes_dont_match(status1a, status1c):
    assert (status1a != status1c) is True


def test___ne___types_dont_match(status1a, priority1):
    assert (status1a != priority1) is True


def test___ne___hashes_change_as_object_changes(client):
    result1 = Result(client)
    result2 = Result(client)
    assert (result1 != result2) is False

    result1.comment = "mock comment a"

    assert (result1 != result2) is True

    result2.comment = "mock comment b"

    assert (result1 != result2) is True

    result2.comment = "mock comment a"

    assert (result1 != result2) is False
