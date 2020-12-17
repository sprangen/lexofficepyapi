=====
Usage
=====

To use lexofficepyAPI in a project::

    from lexofficeapi import LexOffcieAPI

    lexoffice = LexOfficeAPI(api_key="Your API Key")


With this you are authenticated against the https://api.lexoffice.io/ API.


Contacts
========

You can create get and search contacts

Create
------
The simplest example for create would be::

    company = lexoffice.create_compant(name="Name")

Additional options are:
    * tax_number: a String
    * vat_registration_id: a String
    * allow_tax_free_invoices: a Bool
    * role: a String, Defaults to "customer" but can also be "vendor"
    * roles: a List, takes precedence over role and is used if when you want to express that you customer is also a vendor. A valid list would be: `['customer', 'vendor']`
    * contact_salutation: a String - max length is 25 characters
    * contact_first_name: a String - Required
    * contact_last_name: a String - Required
    * contact_primary: a Bool, Defaults to False; if true its shown on the voucher
    * contact_email_address: a String
    * contact_phone_number: a String



.. note::

    There are limitations to the Lexoffice API:

    Please note that it's only possible to create and change contacts with a maximum of one contact person. It's possible to retrieve contacts with more than one contact person, but it's not possible to update such a contact via the REST API.
    https://developers.lexoffice.io/docs/#company-contact-person-details

Get
---

You can get a contact by its ID::

    contact = lexoffice.get_contact(id='aad-asdf-asdf-adf')

Or you can search for it::

    search_results = lexoffice.search_contact(searchTerm="Name")

The search results will be returned as a List, even if only one Item is found.


Invoices
========

You can create Invoices::

    invoice = lexoffice.create_invoice(contactID="asfgs-sdaasdf-adsf", line_item_list=[]):

To create a line_item_list there are two helper class in the dataclasses::

    from lexofficeapi.dataclasses import LineItem, LineText

    line_item = LineItem(name="ItemName", quantity=5, price=10, taxRatePercentage=19, unitName="Unit")
    line_text = LineText(name="Text", description='Text')

But you can also just provice a list that is formed like this::

            [
                {
                  "type": "custom",
                  "name": "Energieriegel Testpaket",
                  "quantity": 1,
                  "unitName": "Stück",
                  "unitPrice": {
                    "currency": "EUR",
                    "netAmount": 5,
                    "taxRatePercentage": 0
                  },
                },
                {
                  "type": "text",
                  "name": "Strukturieren Sie Ihre Belege durch Text-Elemente.",
                  "description": "Das hilft beim Verständnis"
                }
              ]
