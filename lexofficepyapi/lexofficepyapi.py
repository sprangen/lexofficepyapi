"""Main module."""
import requests as requests


class ImproperlyConfigured(Exception):
    pass



class Lexoffice:
    def __init__(self, api_key=None):
        if api_key is None:
            raise ImproperlyConfigured("Lexoffice can not be run without the api_key argument")

        self.api_key = api_key
        self.api_endpoint = "https://api.lexoffice.io/"
        self.api_version = "v1"
        self.base_url = self.api_endpoint + self.api_version + '/'
        self.headers = {"Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept":  "application/json"}


    def get_contact(self, id=None):
        if id is None:
            raise ImproperlyConfigured("Lexoffice needs an id argument to get a contact")
        resource_url = self.base_url + "contacts/" + id
        response = requests.get(resource_url, headers=self.headers)
        return response.json()

    def create_company(self, name=None, taxNumber=None, vatRegistrationId=None, allowTaxFreeInvoices=None, role="customer", roles=None, note=""):

        if name is None:
            raise ImproperlyConfigured("Lexoffice needs at least a name arguemnt to create a company")
        if role != "customer" and role != "vendor":
            raise ImproperlyConfigured("Lexoffice only accepts the roles customer or vendor")
        resource_url = self.base_url + "contacts"

        roles_dict = {}
        if roles is not None:
            if not isinstance(roles, list):
                raise ImproperlyConfigured("Lexoffice only accepts a list for the Argument roles")
            for item in roles:
                if item != "customer" and item != "vendor":
                    raise ImproperlyConfigured("Lexoffice only accepts the roles customer or vendor")
                roles_dict[item] = {}
        else:
            roles_dict[role]= {}


        # This is an example Payload
        #"{
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
                          "taxNumber": taxNumber,
                          "vatRegistrationId": vatRegistrationId,
                          "allowTaxFreeInvoices": allowTaxFreeInvoices,


                      },
                      "note": note
                    }


        response = requests.post(resource_url, json=payload, headers=self.headers)
        id = response.json().get("id")
        return self.get_contact(id)
