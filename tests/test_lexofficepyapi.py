#!/usr/bin/env python

"""Tests for `lexofficepyapi` package."""
import os
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

import pytest
import mock
from lexofficepyapi import Lexoffice
from lexofficepyapi.dataclasses import LineText, LineItem
from lexofficepyapi.exceptions import ImproperlyConfigured


def test_ImproperlyConfigured():
    try:
        Lexoffice()
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_initialization():
    api_key = os.environ.get("API_KEY")
    lexoffice = Lexoffice(api_key=api_key)
    assert lexoffice.api_key == api_key

@pytest.fixture
def lexoffice():
    api_key = os.environ.get("API_KEY")
    return Lexoffice(api_key=api_key)

@pytest.fixture
def company(lexoffice):
    return lexoffice.create_company(name="Testfirma")

def test_raise_if_create_company_has_no_name(lexoffice):
    try:
        lexoffice.create_company()
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_raise_if_create_company_has_a_bad_role(lexoffice):
    try:
        lexoffice.create_company(name="Fail", role="Fail")
    except ImproperlyConfigured:
        pass
    else:
        raise


def test_raise_if_create_company_has_a_bad_roles_list(lexoffice):
    try:
        lexoffice.create_company(name="Fail", roles="Fail")
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_raise_if_create_company_has_a_bad_roles_list_entries(lexoffice):
    try:
        lexoffice.create_company(name="Fail", roles=["fail", "masterfail"])
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_raise_if_create_company_works_with_roles_list_entries(lexoffice):

    company = lexoffice.create_company(name="TestCase", roles=["customer", "vendor"])

    roles = company.get("roles")
    assert roles.get("customer", False)
    assert roles.get("vendor", False)

def test_raise_if_create_company_contact_salutation_is_longer_then_25_chars(lexoffice):

    try:
        lexoffice.create_company(name="TestCase", contact_salutation="abcdefghijklmnopqrstuvwxyz1234567890")
    except ImproperlyConfigured:
        pass
    else:
        raise


def test_raise_if_create_company_contact_with_missing_parameter(lexoffice):

    try:
        lexoffice.create_company(name="TestCase", contact_last_name="Failian")
    except ImproperlyConfigured:
        pass
    else:
        raise


def test_create_company(lexoffice):
    company = lexoffice.create_company(name="Testfirma")

    assert company.get("company").get("name") == "Testfirma"

def test_raise_if_contact_has_no_id(lexoffice):
    try:
        lexoffice.get_contact()
    except ImproperlyConfigured:
        pass
    else:
        raise

def test_retrieve_contact(company, lexoffice):
    contact_id = company.get('id')
    contact =lexoffice.get_contact(contact_id)
    assert contact_id == contact.get('id')


def test_create_company_with_contact_person(lexoffice):

    company = lexoffice.create_company(name="Testfirma", contact_primary=True, contact_salutation="Herr", contact_first_name="Berthold", contact_last_name="Maier",)

    assert company.get("company").get("contactPersons")[0].get('firstName') == "Berthold"



def test_search_contact(lexoffice):

    company = lexoffice.create_company(name="Bike and More")
    search_results = lexoffice.search_contact(searchTerm="Bike")
    assert company.get('id') in search_results


def test_creating_an_invoice(lexoffice):
    company = lexoffice.create_company(name="Heribert AG", )
    line_text = LineText(name="Trenner", description='Beschreibung')
    if datetime.now().year == 2020:
        taxpercentage = "16"
    else:
        taxpercentage = "19"
    price = "10.00"
    line_item = LineItem(name="Item", quantity=5, price=price, taxRatePercentage=taxpercentage, unitName="DSB")

    invoice = lexoffice.create_invoice(company.get('id'), line_item_list=[line_text.to_dict(),line_item.to_dict()])

    assert invoice.get('id')
