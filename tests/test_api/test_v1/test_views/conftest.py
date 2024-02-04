#!/usr/bin/python3
"""Configures tests"""

from pytest import fixture
from api.v1.app import app

@fixture
def client():
  return app.test_client()
  