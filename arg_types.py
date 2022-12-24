import click
from venmo_api import PaymentPrivacy


class PaymentPrivacyArg(click.ParamType):
    name = "payment_privacy"

    def convert(self, value, param, ctx) -> PaymentPrivacy:
        if isinstance(value, PaymentPrivacy):
            return value

        for priv_type in PaymentPrivacy:
            if priv_type.value == value.lower():
                return priv_type
        self.fail("Not a valid PaymentPrivacy value", param, ctx)
