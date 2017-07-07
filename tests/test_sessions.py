import mock
import pytest
import requests
from requests.status_codes import codes

from traw.sessions import Session
from traw import exceptions
from traw.const import GET, BASE_API_PATH as BAP, API_PATH as AP

UNAME = 'mock username'
PWORD = 'mock password'
AUTH = (UNAME, PWORD)
URL = 'http://mock.url'


@pytest.fixture()
def session():
    with mock.patch('traw.sessions.requests') as req_mock:
        sess_mock = mock.create_autospec(requests.Session)
        sess_mock.headers = dict()
        req_mock.Session.return_value = sess_mock

        yield Session(auth=AUTH, url=URL)


@pytest.fixture()
def response():
    yield mock.create_autospec(requests.models.Response)


def test___init__():
    """ Validate the session __init__ """
    with mock.patch('traw.sessions.requests') as req_mock:
        sess_mock = mock.create_autospec(requests.Session)
        sess_mock.headers = dict()
        req_mock.Session.return_value = sess_mock
        session = Session(auth=AUTH, url=URL)

        assert session._auth == AUTH
        assert session._url == URL
        assert session._http is sess_mock
        assert session._http.headers['Content-Type'] == 'application/json'


@mock.patch.object(Session, '_request_with_retries')
def test_request_with_defaults(req_mock, session):
    """ Validate the ``session.request`` method call """
    REQ_RESP = {'key': 'value'}
    req_mock.return_value = REQ_RESP
    response = session.request(method=GET, path=AP['get_projects'])

    exp_url = URL + BAP + '/' + AP['get_projects']
    exp_call = mock.call(method=GET, params={}, url=exp_url, json=None)

    assert response is REQ_RESP
    assert req_mock.call_args == exp_call


@mock.patch.object(Session, '_request_with_retries')
def test_request_with_params(req_mock, session):
    """ Validate the ``session.request`` method call with params"""
    REQ_RESP = {'key': 'value'}
    req_mock.return_value = REQ_RESP
    PARAM = {'param_key': 'param_val'}
    JSON = {'json_key': 'json_val'}
    response = session.request(
        method=GET, path=AP['get_projects'], params=PARAM, json=JSON)

    exp_url = URL + BAP + '/' + AP['get_projects']
    exp_call = mock.call(method=GET, params=PARAM, url=exp_url, json=JSON)

    assert response is REQ_RESP
    assert req_mock.call_args == exp_call


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_bad_gateway(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for bad_gateway """
    response.status_code = codes['bad_gateway']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.ServerError):
        session._request_with_retries()

    assert make_req_mock.call_count == 3


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_bad_request(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for bad_request """
    response.status_code = codes['bad_request']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.BadRequest):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_conflict(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for bad_request """
    response.status_code = codes['conflict']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.Conflict):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_found(make_req_mock, session):
    """ Validate _request_with_retries exception logic for bad_request """
    MOCK_URL = 'http://mock.domain/mock_loc'
    MOCK_LOC = '/mock_loc'
    response = mock.MagicMock()
    response.status_code = codes['found']
    response.headers = dict()
    response.headers['location'] = MOCK_URL
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.Redirect) as exc:
        session._request_with_retries()

    assert make_req_mock.call_count == 1
    assert exc.value.path == MOCK_LOC


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_forbidden(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for forbidden """
    response.status_code = codes['forbidden']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.Forbidden):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_gateway_timeout(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for gateway_timeout """
    response.status_code = codes['gateway_timeout']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.ServerError):
        session._request_with_retries()

    assert make_req_mock.call_count == 3


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_internal_serv_err(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for internal_server_error """
    response.status_code = codes['internal_server_error']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.ServerError):
        session._request_with_retries()

    assert make_req_mock.call_count == 3


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_not_found(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for not_found """
    response.status_code = codes['not_found']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.NotFound):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_req_too_large(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for req_too_large """
    response.status_code = codes['request_entity_too_large']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.TooLarge):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_service_unavailable(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for service_unavailable """
    response.status_code = codes['service_unavailable']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.ServerError):
        session._request_with_retries()

    assert make_req_mock.call_count == 3


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_unauthorized(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for unauthorized """
    response.status_code = codes['unauthorized']
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.Forbidden):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_no_content(make_req_mock, session, response):
    """ Validate _request_with_retries logic for no_content """
    response.status_code = codes['no_content']
    make_req_mock.return_value = response, None

    result = session._request_with_retries()

    assert result is None
    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_unknown_status_code(make_req_mock, session, response):
    """ Validate _request_with_retries exception logic for unknown status code """
    response.status_code = 666
    make_req_mock.return_value = response, None

    with pytest.raises(exceptions.UnknownStatusCode):
        session._request_with_retries()

    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_zero_len_header(make_req_mock, session):
    """ Validate _request_with_retries logic for zero length response """
    response = mock.MagicMock()
    response.status_code = codes['ok']
    response.headers = dict()
    response.headers['content-length'] = '0'
    make_req_mock.return_value = response, None

    result = session._request_with_retries()

    assert result == ''
    assert make_req_mock.call_count == 1


@mock.patch.object(Session, '_make_request')
def test_req_w_retries_valid_content(make_req_mock, session):
    """ Validate _request_with_retries exception logic for valid content """
    exp_dict = {'key': 'value'}
    response = mock.MagicMock()
    response.status_code = codes['ok']
    response.headers = dict()
    response.headers['content-length'] = '100'
    response.json.return_value = exp_dict
    make_req_mock.return_value = response, None

    result = session._request_with_retries()

    assert result == exp_dict
    assert make_req_mock.call_count == 1


def test__make_request_exc(session):
    """ Validate _make_request handles exceptions """
    session._http.request.side_effect = ValueError
    resp, exc = session._make_request(method='method', url='url')

    assert resp is None
    assert isinstance(exc, ValueError)


def test__make_request_valid_response(session, response):
    """ Validate _make_request returns response """
    session._http.request.return_value = response

    resp, exc = session._make_request(method='method', url='url')

    assert resp is response
    assert exc is None


def test_close(session):
    """ Validate close call """
    session.close()

    assert session._http.close.called
