"""Main module."""
from dataclasses import dataclass, asdict
from datetime import datetime

import requests as requests


from lexofficepyapi.dataclasses import Person
from lexofficepyapi.exceptions import ImproperlyConfigured


class Lexoffice:
    def __init__(self, api_key=None):
        if api_key is None:
            raise ImproperlyConfigured(
                "Lexoffice can not be run without the api_key argument"
            )

        self.api_key = api_key
        self.api_endpoint = "https://api.lexoffice.io/"
        self.api_version = "v1"
        self.base_url = self.api_endpoint + self.api_version + "/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_contact(self, id=None):
        if id is None:
            raise ImproperlyConfigured(
                "Lexoffice needs an id argument to get a contact"
            )
        resource_url = self.base_url + "contacts/" + id
        response = requests.get(resource_url, headers=self.headers)
        return response.json()

    def search_contact(self, searchTerm):
        page_number = 0
        resource_url = self.base_url + f"contacts/?page={page_number}"
        search_results = []
        response = requests.get(resource_url, headers=self.headers)
        response_json = response.json()
        page_range = response_json.get("totalPages")
        contact_list = response_json.get("content")
        for page in range(page_range):
            page_number = page
            resource_url = self.base_url + f"contacts/?page={page_number}"
            response = requests.get(resource_url, headers=self.headers)
            response_json = response.json()
            contact_list + response_json.get("content")

        for contact in contact_list:
            contact_id = contact.get('id')
            if contact.get("company"):
                details = contact.get("company")
            else:
                details = contact.get('person')
            for key, value in details.items():
                if value == searchTerm:
                    search_results.append(contact_id)
                elif isinstance(value, str):
                    if searchTerm in value:
                        search_results.append(contact_id)

        return search_results


    def get_invoice(self, id=None):
        if id is None:
            raise ImproperlyConfigured(
                "Lexoffice needs an id argument to get an invoice"
            )
        resource_url = self.base_url + "invoices/" + id
        response = requests.get(resource_url, headers=self.headers)
        return response.json()

    def create_company(
        self,
        name: str = None,
        tax_number: str = None,
        vat_registration_id: str = None,
        allow_tax_free_invoices: bool = None,
        role="customer",
        roles=None,
        contact_salutation: str = None,
        contact_first_name: str = None,
        contact_last_name: str = None,
        contact_primary: bool = False,
        contact_email_address: str = None,
        contact_phone_number: str= None,

        note="",
    ):

        if name is None:
            raise ImproperlyConfigured(
                "Lexoffice needs at least a name arguemnt to create a company"
            )
        if role != "customer" and role != "vendor":
            raise ImproperlyConfigured(
                "Lexoffice only accepts the roles customer or vendor"
            )

        resource_url = self.base_url + "contacts"

        roles_dict = {}
        if roles is not None:
            if not isinstance(roles, list):
                raise ImproperlyConfigured(
                    "Lexoffice only accepts a list for the Argument roles"
                )
            for item in roles:
                if item != "customer" and item != "vendor":
                    raise ImproperlyConfigured(
                        "Lexoffice only accepts the roles customer or vendor"
                    )
                roles_dict[item] = {}
        else:
            roles_dict[role] = {}

        contact_person = Person(
            salutation=contact_salutation,
            firstName=contact_first_name,
            lastName=contact_last_name,
            emailAddress=contact_email_address,
            phoneNumber=contact_phone_number,
            primary=contact_primary
        )

        contact_person.validate()
        if contact_person.empty():
            contact_person = []
        else:
            contact_person = asdict(contact_person)
            contact_person = [contact_person]


        # This is an example Payload
        # "{
        # "roles": {
        # "customer": {},
        # "vendor":
        # {    }
        #   },
        #   "company": {
        #     "name": "Testfirma",
        #     "taxNumber": "12345/12345",
        #     "vatRegistrationId": "DE123456789",
        #     "allowTaxFreeInvoices": true,
        #     "contactPersons": [
        #       {
        #         "salutation": "Herr",
        #         "firstName": "Max",
        #         "lastName": "Mustermann",
        #         "emailAddress": "contactpersonmail@lexoffice.de",
        #         "phoneNumber": "08000/11111"
        #       }
        #     ]
        #   },
        #   "addresses": {
        #     "billing": [
        #       {
        #         "supplement": "Rechnungsadressenzusatz",
        #         "street": "Hauptstr. 5",
        #         "zip": "12345",
        #         "city": "Musterort",
        #         "countryCode": "DE"
        #       }
        #     ],
        #     "shipping": [
        #       {
        #         "supplement": "Lieferadressenzusatz",
        #         "street": "Schulstr. 13",
        #         "zip": "76543",
        #         "city": "MUsterstadt",
        #         "countryCode": "DE"
        #       }
        #     ]
        #   },
        #   "emailAddresses": {
        #     "business": [
        #       "business@lexoffice.de"
        #     ],
        #     "office": [
        #       "office@lexoffice.de"
        #     ],
        #     "private": [
        #       "private@lexoffice.de"
        #     ],
        #     "other": [
        #       "other@lexoffice.de"
        #     ]
        #   },
        #   "phoneNumbers": {
        #     "business": [
        #       "08000/1231"
        #     ],
        #     "office": [
        #       "08000/1232"
        #     ],
        #     "mobile": [
        #       "08000/1233"
        #     ],
        #     "private": [
        #       "08000/1234"
        #     ],
        #     "fax": [
        #       "08000/1235"
        #     ],
        #     "other": [
        #       "08000/1236"
        #     ]
        #   },
        #   "note": "Notizen"
        # }"
        payload = {
            "version": 0,
            "roles": roles_dict,
            "company": {
                "name": name,
                "taxNumber": tax_number,
                "vatRegistrationId": vat_registration_id,
                "allowTaxFreeInvoices": allow_tax_free_invoices,
                "contactPersons": contact_person
            },
            "addresses": {
                "billing": [{}],
                "shipping": [{}]
            },
            "phoneNumbers": {},
            "note": note,
        }
        results = self.search_contact(searchTerm=name)
        if len(results) > 0:
            return self.get_contact(results[0])
        response = requests.post(resource_url, json=payload, headers=self.headers)
        id = response.json().get("id")
        return self.get_contact(id)


    def create_invoice(self, contactID, line_item_list):
        """
        Sample Payload:
         '
            {
             "archived": false,
              "voucherDate": "2017-02-22T00:00:00.000+01:00",
               "address": {
               "name": "Bike & Ride GmbH & Co. KG",
                "supplement": "Gebäude 10",
                "street": "Musterstraße 42",
                "city": "Freiburg",
                "zip": "79112",
                "countryCode": "DE"
              },
              "lineItems": [
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
                  "discountPercentage": 0
                },
                {
                  "type": "text",
                  "name": "Strukturieren Sie Ihre Belege durch Text-Elemente.",
                  "description": "Das hilft beim Verständnis"
                }
              ],
              "totalPrice": {
                "currency": "EUR"
               },
              "taxConditions": {
                "taxType": "net"
              },
              "paymentConditions": {
                "paymentTermLabel": "10 Tage - 3 %, 30 Tage netto",
                "paymentTermDuration": 30,
                "paymentDiscountConditions": {
                  "discountPercentage": 3,
                  "discountRange": 10
                }
              },
              "shippingConditions": {
                "shippingDate": "2017-04-22T00:00:00.000+02:00",
                "shippingType": "delivery"
              },
              "title": "Rechnung",
              "introduction": "Ihre bestellten Positionen stellen wir Ihnen hiermit in Rechnung",
              "remark": "Vielen Dank für Ihren Einkauf"
            }
            '
        """

        lexware_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000+00:00')
        payload = {
            "voucherDate": lexware_now,
            "address": {
                "contactId": contactID,
            },
            "lineItems": line_item_list,
            "totalPrice": {
                "currency": "EUR"
            },
            "taxConditions": {
                "taxType": "net"
            },
            "shippingConditions": {
                "shippingDate": lexware_now,
                "shippingType": "service"
            },
        }
        resource_url = self.base_url + 'invoices'

        response = requests.post(resource_url, json=payload, headers=self.headers)
        id = response.json().get("id")

        return self.get_invoice(id)
