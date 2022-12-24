# venmo-cli
venmo-cli is a simple CLI for Venmo, built on the [Venmo API](https://github.com/mmohades/Venmo) by mmohades. As with his API, use this tool _at your own risk_ as it is **not** sponsored/maintained by PayPal or Venmo.

## Sample usage

```
$ venmo --help
Usage: venmo [OPTIONS] COMMAND [ARGS]...

  venmo-cli: Venmo for the command-line

Options:
  --help  Show this message and exit.

Commands:
  logout   Logs out of your current session
  pay      Sends money to another user
  request  Requests money from another user
```

```
$ venmo pay --help
Usage: venmo pay [OPTIONS] USERNAME

  Sends money to another user

Options:
  -a, --amount FLOAT             [required]
  -m, --msg TEXT                 [default: 🤖]
  -p, --privacy PAYMENT_PRIVACY  [default: friends]
  --help                         Show this message and exit.
```

```bash
$ venmo pay cameronbernhardt -a 5 -m "thanks for the pizza" --privacy=private
```

```bash
$ venmo request cameronbernhardt -a 10 -m "lunch"
```