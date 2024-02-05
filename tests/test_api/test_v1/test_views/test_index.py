#!/usr/bin/python3
"""Routes test cases for index.py"""


def get_status(client):
    response = client.get('/api/v1/status')
    assert b'{"status": "OK"}' in response.data
