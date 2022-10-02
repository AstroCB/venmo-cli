#! /usr/local/bin/python3

import argparse
import getpass
import os
import pickle
import sys

from venmo_api import Client, PaymentPrivacy

TOKEN_PATH = "token.pickle"


class Venmo:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Venmo for the command-line",
        )
        parser.add_argument("subcommand", help="Subcommand to run")

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.subcommand):
            print("Unrecognized command")
            parser.print_help()
            exit(1)

        self.client = Venmo._get_client()

        getattr(self, args.subcommand)()

    def _get_client():
        access_token = ""
        if os.path.exists(TOKEN_PATH):
            # Existing cached access token
            with open(TOKEN_PATH, "rb") as f:
                access_token = pickle.load(f)
        else:
            # Fresh login
            user = input("Venmo email: ")
            pwrd = getpass.getpass("Venmo password: ")
            access_token = Client.get_access_token(username=user, password=pwrd)

            # Cache access token
            with open(TOKEN_PATH, "wb") as f:
                pickle.dump(access_token, f)

        return Client(access_token=access_token)

    def _get_subargs(parser):
        # ignore the executable itself and the subcommand
        # to get the subcommand arguments
        return parser.parse_args(sys.argv[2:])

    def _get_user(self, username):
        user = self.client.user.get_user_by_username(username)
        if user is None:
            print("User not found")
            exit(1)
        return user

    def request(self):
        parser = argparse.ArgumentParser(description="Request money from another user")
        parser.add_argument("-a", "--amount", type=int, required=True)
        parser.add_argument("-u", "--user", type=str, required=True)
        parser.add_argument("-m", "--msg", type=str, default="🤖")
        parser.add_argument(
            "-p", "--privacy", type=PaymentPrivacy, default=PaymentPrivacy.FRIENDS
        )

        args = Venmo._get_subargs(parser)
        user = self._get_user(args.user)
        self.client.payment.request_money(
            args.amount, args.msg, target_user=user, privacy_setting=args.privacy
        )


if __name__ == "__main__":
    Venmo()