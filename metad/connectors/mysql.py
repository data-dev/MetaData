import os
from collections import defaultdict

import pandas as pd
import pymysql

from metad import MetaData
from metad.connectors.base import BaseConnector


class MySQLConnector(BaseConnector):
    """Import data from MySQL instances.

    The MySQLConnector allows you to import data from a MySQL instance
    by translating the data types and exporting the primary / foreign key
    constraints from the schema table.
    """

    def __init__(self, host, port, user, password, database):
        """Create a new MySQLConnector.

        Args:
            host (str): The host name / ip address of the MySQL instance.
            port (int): The port number (default: 3306).
            user (str): The username for accessing the instance.
            password (str): The password for accessing the instance.
            database (str): The name of the database to export.
        """
        super().__init__()
        self.database = database
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=database,
            charset='utf8'
        )
        self._load_metadata()

    def __del__(self):
        self.db.close()

    def _load_metadata(self):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.metadata = MetaData()
        self.metadata.set_tables(self._tables(cursor))
        self.metadata.set_foreign_keys(self._foreign_keys(cursor))
        cursor.close()

    def export_metadata(self, path_to_json):
        self.metadata.to_json(path_to_json)

    def export_tables(self, path_to_output):
        for table in self.metadata.data["tables"]:
            cursor = self.db.cursor(pymysql.cursors.Cursor)
            cursor.execute("select * from `" + table["name"] + "`;")
            column_names = [column[0] for column in cursor.description]
            rows = [list(row) for row in cursor.fetchall()]
            df = pd.DataFrame(rows, columns=column_names)
            df.to_csv(
                os.path.join(
                    path_to_output,
                    "%s.csv" %
                    table["name"]),
                index=False)
            cursor.close()

    def _tables(self, cursor):
        tables = []
        for table_name in self._table_names(cursor):
            tables.append(self._table_metadata(cursor, table_name))
        return tables

    def _foreign_keys(self, cursor):
        # Select Foreign Key Constraints
        cursor.execute("""SELECT
            CONSTRAINT_NAME,
            TABLE_NAME,
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE
            REFERENCED_TABLE_SCHEMA = '%s'""" % self.database)
        foreign_keys = cursor.fetchall()

        # Aggregate Composite Keys
        foreign_key_constraints = defaultdict(list)
        for row in foreign_keys:
            foreign_key_constraints[row["CONSTRAINT_NAME"]].append(row)

        for constraint_name, constraint_rows in list(
                foreign_key_constraints.items()):
            constraint = {
                "table": None,
                "field": [],
                "ref_table": None,
                "ref_field": []
            }
            for row in constraint_rows:
                constraint["table"] = row["TABLE_NAME"]
                constraint["field"].append(row["COLUMN_NAME"])
                constraint["ref_table"] = row["REFERENCED_TABLE_NAME"]
                constraint["ref_field"].append(row["REFERENCED_COLUMN_NAME"])

            # Simplify Non-Composite Keys
            if len(constraint["field"]) == 1:
                constraint["field"] = constraint["field"][0]
                constraint["ref_field"] = constraint["ref_field"][0]
            foreign_key_constraints[constraint_name] = constraint

        return list(foreign_key_constraints.values())

    def _table_names(self, cursor):
        cursor.execute("show tables;")
        table_names = []
        for row in cursor.fetchall():
            table_names.append(list(row.values())[0])
        return table_names

    def _table_metadata(self, cursor, table_name):
        cursor.execute("""
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE
                table_name = '%s' AND
                table_schema = '%s'
            ORDER BY ORDINAL_POSITION""" % (table_name, self.database))
        fields = []
        primary_key = []
        for row in cursor.fetchall():
            data_type = {
                "int": "numerical",
                "tinyint": "numerical",
                "smallint": "numerical",
                "enum": "categorical",
                "bit": "categorical",
                "binary": "categorical",
                "varchar": "text",
                "text": "text",
                "tinytext": "text",
                "longtext": "text",
                "mediumtext": "text",
                "char": "text",
                "datetime": "datetime",
                "year": "datetime",
                "timestamp": "datetime",
                "time": "datetime",
                "float": "numerical",
                "double": "numerical",
                "bigint": "numerical",
                "mediumint": "numerical",
                "decimal": "numerical",
                "date": "datetime",
                "blob": "other",
                "mediumblob": "other",
                "longblob": "other",
                "set": "other",
                "geometry": "other"
            }[row["DATA_TYPE"]]
            if row["COLUMN_KEY"] == "PRI":
                primary_key.append(row["COLUMN_NAME"])
            fields.append({
                "name": row["COLUMN_NAME"],
                "data_type": data_type
            })
        if len(primary_key) == 1:
            primary_key = primary_key[0]
        table = {
            "name": table_name,
            "fields": fields
        }
        if primary_key:
            table["primary_key"] = primary_key[0] if len(
                primary_key) == 1 else primary_key

        return {
            "name": table_name,
            "primary_key": primary_key,
            "fields": fields
        }
