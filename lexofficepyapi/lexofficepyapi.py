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

    def create_company(self, name=None, role="customer", note=""):

        if name is None:
            raise ImproperlyConfigured("Lexoffice needs at least a name arguemnt to create a company")
        resource_url = self.base_url + "contacts"
        #"{\n  \"roles\": {\n    \"customer\": {\n    },\n    \"vendor\": {\n    }\n  },\n  \"company\": {\n    \"name\": \"Testfirma\",\n    \"taxNumber\": \"12345/12345\",\n    \"vatRegistrationId\": \"DE123456789\",\n    \"allowTaxFreeInvoices\": true,\n    \"contactPersons\": [\n      {\n        \"salutation\": \"Herr\",\n        \"firstName\": \"Max\",\n        \"lastName\": \"Mustermann\",\n        \"emailAddress\": \"contactpersonmail@lexoffice.de\",\n        \"phoneNumber\": \"08000/11111\"\n      }\n    ]\n  },\n  \"addresses\": {\n    \"billing\": [\n      {\n        \"supplement\": \"Rechnungsadressenzusatz\",\n        \"street\": \"Hauptstr. 5\",\n        \"zip\": \"12345\",\n        \"city\": \"Musterort\",\n        \"countryCode\": \"DE\"\n      }\n    ],\n    \"shipping\": [\n      {\n        \"supplement\": \"Lieferadressenzusatz\",\n        \"street\": \"Schulstr. 13\",\n        \"zip\": \"76543\",\n        \"city\": \"MUsterstadt\",\n        \"countryCode\": \"DE\"\n      }\n    ]\n  },\n  \"emailAddresses\": {\n    \"business\": [\n      \"business@lexoffice.de\"\n    ],\n    \"office\": [\n      \"office@lexoffice.de\"\n    ],\n    \"private\": [\n      \"private@lexoffice.de\"\n    ],\n    \"other\": [\n      \"other@lexoffice.de\"\n    ]\n  },\n  \"phoneNumbers\": {\n    \"business\": [\n      \"08000/1231\"\n    ],\n    \"office\": [\n      \"08000/1232\"\n    ],\n    \"mobile\": [\n      \"08000/1233\"\n    ],\n    \"private\": [\n      \"08000/1234\"\n    ],\n    \"fax\": [\n      \"08000/1235\"\n    ],\n    \"other\": [\n      \"08000/1236\"\n    ]\n  },\n  \"note\": \"Notizen\"\n}"
        payload = {
                      "version": 0,
                      "roles": {
                        role: {
                        }
                      },
                      "company": {
                         "name": name,
                      },
                      "note": note
                    }


        response = requests.post(resource_url, json=payload, headers=self.headers)
        id = response.json().get("id")
        return self.get_contact(id)
