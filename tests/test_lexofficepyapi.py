#!/usr/bin/env python

"""Tests for `lexofficepyapi` package."""
import os

import pytest
import mock
from lexofficepyapi import Lexoffice
from lexofficepyapi.lexofficepyapi import ImproperlyConfigured


def test_ImproperlyConfigured():
    try:
        Lexoffice()
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_initialization():
    api_key = os.environ.get("api_key")
    lexoffice = Lexoffice(api_key=api_key)
    assert lexoffice.api_key == api_key

@pytest.fixture
def lexoffice():
    api_key = os.environ.get("api_key")
    return Lexoffice(api_key=api_key)


def test_create_company(lexoffice):
    company = lexoffice.create_company(name="Testfirma")

    assert company.get("company").get("name") == "Testfirma"

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
