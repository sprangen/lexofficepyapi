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

Additional options to name are:
    * tax_number: a String
    * vat_registration_id: a String
    * allow_tax_free_invoices: a Bool
    * role: a String, Defaults to "customer" but can also be "vendor"
    * roles: a List, takes precedence over role and is used if when you want to express that you customer is also a vendor. A valid list would be: `['customer', 'vendor']`
