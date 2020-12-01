=====
Usage
=====

To use lexofficepyAPI in a project::

    from lexofficeapi import LexOffcieAPI

    lexoffice = LexOfficeAPI(api_key="Your API Key")


With this you are authenticated against the https://api.lexoffice.io/ API.


Contacts
========

You can create, update, get and filter contacts

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

