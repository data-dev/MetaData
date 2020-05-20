"""MetaData CLI.

Usage:
  metad describe <json>
  metad validate <jsons>...
  metad rdr --database=<database>
  metad mysql --host=<host> --port=<port> --user=<user> --password=<password> --database=<database>

Options:
  -h --help              Show this screen.
  --host <host>          The MySQL host.
  --port <port>          The MySQL port.
  --user <user>          The MySQL username.
  --password <password>  The MySQL password.
  --database <database>  The MySQL database name.
"""
from docopt import docopt

from metad import MetaData
from metad.connectors import MySQLConnector


def describe(args):
    metadata = MetaData.from_json(args["<json>"])
    print(str(metadata))


def validate(args):
    for path_to_json in args["<jsons>"]:
        print("Validating %s..." % path_to_json)
        MetaData.from_json(path_to_json).validate()


def mysql(args):
    connector = MySQLConnector(
        host=args["--host"],
        port=args["--port"],
        user=args["--user"],
        password=args["--password"],
        database=args["--database"],
    )
    connector.export(args["--database"])


def rdr(args):
    connector = MySQLConnector(
        host='relational.fit.cvut.cz',
        port=3306,
        user='guest',
        password='relational',
        database=args["--database"],
    )
    connector.export(args["--database"])


def main():
    args = docopt(__doc__)
    if args["describe"]:
        describe(args)
    elif args["validate"]:
        validate(args)
    elif args["mysql"]:
        mysql(args)
    elif args["rdr"]:
        rdr(args)


if __name__ == '__main__':
    main()
