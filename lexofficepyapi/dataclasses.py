from dataclasses import asdict, dataclass
from decimal import Decimal

from lexofficepyapi.exceptions import ImproperlyConfigured


@dataclass
class Person:
    salutation: str
    firstName: str
    lastName: str
    emailAddress: str
    phoneNumber: str
    primary: bool

    def empty(self):
        for key, value in asdict(self).items():
            if value:
                return False
        return True


    def validate_salutation(self):
        if len(self.salutation) > 25:
            raise ImproperlyConfigured(
                "Lexoffice only accepts a Salutation with lesser then 25 Chars"
            )

    def validate(self):
        if self.salutation:
            self.validate_salutation()

        to_validate = not(self.empty())

        if to_validate:
            for key, value in asdict(self).items():
                if key == 'salutation':
                    pass
                elif key == "emailAddress":
                    pass
                elif key == "phoneNumber":
                    pass
                elif value is None:
                    raise ImproperlyConfigured(
                        f"Lexoffice needs {key} to create a Company Contact"
                    )


@dataclass
class LineText():
    type = "text"
    name: str
    description: str

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description
        }

@dataclass
class LineItem():
    type = "custom"
    name: str
    quantity: int
    unitName: str
    price: str
    taxRatePercentage: str

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "quantity": self.quantity,
            "unitName": self.unitName,
            "unitPrice": {
                "currency": "EUR",
                "netAmount": self.price,
                "taxRatePercentage": self.taxRatePercentage
            }
        }
