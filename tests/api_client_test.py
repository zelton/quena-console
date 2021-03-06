import requests
from expects import *
from mockito import mock

from app.cli import ApiClient


def it_retrieves_entries_filtered_with_a_phrase(when, unstub):
    test_json = [
        {
            'id': 1,
            'title': 'A?',
            'content': 'B'
        }
    ]
    response = mock(spec=requests.Response)
    when(response).json().thenReturn(test_json)
    when(requests).get('http://localhost:8000/api/entries.json?title=a').thenReturn(response)

    client = ApiClient('http://localhost:8000')

    expect(client.search_entries_for('a')).to(equal(test_json))


def it_raises_exception_when_getting_error_http_code(when, unstub):
    response = mock(spec=requests.Response)
    when(requests).get('http://localhost:8000/api/entries.json?title=a').thenReturn(response)
    when(response).raise_for_status().thenRaise(requests.exceptions.RequestException)

    client = ApiClient('http://localhost:8000')

    expect(lambda: client.search_entries_for('a')).to(raise_error(requests.exceptions.RequestException))
