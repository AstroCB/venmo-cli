#! /usr/local/bin/python3

import getpass
import os
import pickle

from venmo_api import Client, PaymentPrivacy
import click

from arg_types import PaymentPrivacyArg

TOKEN_PATH = "token.pickle"


class Venmo:
    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        if os.path.exists(TOKEN_PATH):
            # Existing cached access token
            with open(TOKEN_PATH, "rb") as f:
                self.access_token = pickle.load(f)
        else:
            # Fresh login
            user = input("Venmo email: ")
            pwrd = getpass.getpass("Venmo password: ")
            self.access_token = Client.get_access_token(username=user, password=pwrd)

            # Cache access token
            with open(TOKEN_PATH, "wb") as f:
                pickle.dump(self.access_token, f)

        return Client(access_token=self.access_token)

    def _get_user(self, username):
        user = self.client.user.get_user_by_username(username)
        if user is None:
            print("User not found")
            exit(1)
        return user

    def logout(self):
        if not self.client.log_out(self.access_token):
            print("Failed to log out of Venmo session")
            exit(1)

        os.remove(TOKEN_PATH)
        print("Successfully logged out of Venmo session")


@click.group(help="venmo-cli: Venmo for the command-line")
@click.pass_context
def cli(ctx):
    ctx.obj = Venmo()


def enum_values(enum):
    return [case.value for case in enum]


# Decorator for commands that process money (request/pay)
# with common args used for both
def payment_command(f):
    @click.argument("username")
    @click.option("-a", "--amount", type=float, required=True)
    @click.option("-m", "--msg", default="🤖", show_default=True)
    @click.option(
        "-p",
        "--privacy",
        type=PaymentPrivacyArg(),
        default=PaymentPrivacy.FRIENDS.value,
        show_default=True,
    )
    @click.pass_obj
    def process_args(venmo, username, amount, msg, privacy):
        f(venmo, username, amount, msg, privacy)

    return process_args


@cli.command(name="request", help="Requests money from another user")
@payment_command
def request(venmo: Venmo, username, amount, msg, privacy):
    user = venmo._get_user(username)
    venmo.client.payment.request_money(
        amount, msg, target_user=user, privacy_setting=privacy
    )


@cli.command(name="pay", help="Sends money to another user")
@payment_command
def pay(venmo: Venmo, username, amount, msg, privacy):
    user = venmo._get_user(username)
    venmo.client.payment.send_money(
        amount, msg, target_user=user, privacy_setting=privacy
    )


@cli.command(help="Logs out of your current session")
@click.pass_obj
def logout(venmo: Venmo):
    venmo.logout()


if __name__ == "__main__":
    cli()
